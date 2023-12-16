from __future__ import annotations

import asyncio
import os
from enum import Enum

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech.audio import AudioStreamFormat
from dotenv import load_dotenv

from app.utils.logging_util import logger


class AzureLanguageCode(str, Enum):
    """Enum for all supported Azure languages"""

    DE_CH = "de-CH"
    DE_DE = "de-DE"
    DE_AT = "de-AT"
    EN_GB = "en-GB"
    EN_US = "en-US"


class AzureUtil(object):
    """Singleton util class to handle various speech to text related operations with azure"""

    _instance = None
    speech_config: SpeechConfig
    azure_region: str
    azure_speech_Key: str
    language_code: AzureLanguageCode

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AzureUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, language_code: AzureLanguageCode = AzureLanguageCode.DE_CH):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        if (
            os.getenv("AZURE_REGION") is None
            or os.getenv("AZURE_SPEECH_RESOURCE_KEY") is None
        ):
            raise EnvironmentError(
                ".env file is missing the AZURE_SPEECH_RESOURCE_KEY or AZURE_REGION"
            )
        else:
            self.azure_region = os.getenv("AZURE_REGION")
            self.azure_speech_Key = os.getenv("AZURE_SPEECH_RESOURCE_KEY")
            self.language_code = language_code

            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_Key,
                region=self.azure_region,
                speech_recognition_language=self.language_code,
            )
        logger.info("Created AzureUtil")
        self._initialized = True

    async def transcribe_with_push_stream(
        self,
        data: bytes,
        params,
        use_diarization: bool = False,
        language: AzureLanguageCode = AzureLanguageCode.DE_CH,
    ):
        """Azure continuous recognition/diarization for a Spooled File with a push stream"""
        self.speech_config.speech_recognition_language = language
        # self.speech_config.output_format = speechsdk.OutputFormat.Detailed
        # get the correct audio format
        audio_format = AudioStreamFormat(
            channels=params.nchannels,
            samples_per_second=params.framerate,
            bits_per_sample=params.sampwidth * 8,
        )
        # get the push stream
        stream = speechsdk.audio.PushAudioInputStream(audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the correct recognizer based on diarization flag
        if use_diarization:
            recognizer = speechsdk.transcription.ConversationTranscriber(
                speech_config=self.speech_config, audio_config=audio_config
            )
        else:
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config, audio_config=audio_config
            )

        # create callbacks
        recognized_queue: asyncio.Queue[
            speechsdk.SpeechRecognitionEventArgs
        ] = asyncio.Queue()
        done = False

        def yield_event(event: speechsdk.SpeechRecognitionEventArgs):
            logger.debug(f"{event}")
            if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_queue.put_nowait(event)
            elif event.result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = event.result.cancellation_details
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logger.error(cancellation_details.error_details)

        def print_event(event: speechsdk.SpeechRecognitionEventArgs):
            logger.debug(f"{event}")

        def stop_cb(event: speechsdk.SessionEventArgs):
            """callback that signals to stop continuous recognition/diarization upon receiving an event `evt`"""
            logger.debug(f"CLOSING {event}")
            nonlocal done
            done = True

        # subscribe to the events based on diarization flag
        final_event_type = "transcribed" if use_diarization else "recognized"
        intermediate_event_type = "transcribing" if use_diarization else "recognizing"
        getattr(recognizer, final_event_type).connect(yield_event)
        getattr(recognizer, intermediate_event_type).connect(print_event)
        recognizer.session_started.connect(print_event)
        recognizer.session_stopped.connect(print_event)
        recognizer.canceled.connect(print_event)
        # stop events
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        # start continuous speech recognition/diarization and write data to stream
        if use_diarization:
            recognizer.start_transcribing_async()
        else:
            recognizer.start_continuous_recognition()

        logger.info(
            f"Starting Azure Recognition [language={language}, diarization={use_diarization}]"
        )
        stream.write(data)
        stream.close()

        # process data
        try:
            while not done or not recognized_queue.empty():
                # read from queue if not empty
                if not recognized_queue.empty():
                    item = await recognized_queue.get()
                    text = getattr(item.result, "text", "")
                    if use_diarization:
                        yield f"{getattr(item.result, 'speaker_id', '')}: {text}\n"
                    else:
                        yield f"{text} "
                await asyncio.sleep(0.1)
        finally:
            # stop recognition/diarization and clean up
            logger.info(
                f"Stopping Azure Recognition [language={language}, diarization={use_diarization}]"
            )
            if use_diarization:
                recognizer.stop_transcribing_async()
            else:
                recognizer.stop_continuous_recognition()
            # get remaining data
            if not recognized_queue.empty():
                item = await recognized_queue.get()
                text = getattr(item.result, "text", "")
                if use_diarization:
                    yield f"{getattr(item.result, 'speaker_id', '')}: {text}\n"
                else:
                    yield f"{text} "
            logger.info("Stopped Azure Recognition")
