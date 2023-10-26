from __future__ import annotations

import asyncio
import json
import os
from enum import Enum

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech.audio import AudioStreamFormat
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi import WebSocket, WebSocketDisconnect

from app.utils.logging_util import logger


class LanguageCode(str, Enum):
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
    language_code: LanguageCode

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AzureUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, language_code: LanguageCode = LanguageCode.DE_CH):
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

    def azure_short_s2t(self, file_path: str):
        """Azure single-shot recognition for an existing audio file. Max length is 15 seconds"""
        audio_config = speechsdk.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )
        result = speech_recognizer.recognize_once_async().get()
        return result

    async def speech_recognition_with_push_stream(self, file: UploadFile, params):
        """Azure continuous recognition for a Spooled File with a push stream"""
        # get the correct audio format
        audio_format = AudioStreamFormat(
            channels=params.nchannels,
            samples_per_second=params.framerate,
            bits_per_sample=params.sampwidth * 8,
        )
        # get the push stream
        stream = speechsdk.audio.PushAudioInputStream(audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        # register callbacks
        recognized_queue: asyncio.Queue[
            speechsdk.SpeechRecognitionEventArgs
        ] = asyncio.Queue()
        done = False

        def yield_event(event: speechsdk.SpeechRecognitionEventArgs):
            logger.info(f"{event}")
            recognized_queue.put_nowait(event)

        def print_event(event: speechsdk.SpeechRecognitionEventArgs):
            logger.debug(f"{event}")

        def stop_cb(event: speechsdk.SessionEventArgs):
            """callback that signals to stop continuous transcription upon receiving an event `evt`"""
            print(f"CLOSING {event}")
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(yield_event)
        speech_recognizer.recognizing.connect(yield_event)
        speech_recognizer.session_started.connect(print_event)
        speech_recognizer.session_stopped.connect(print_event)
        speech_recognizer.canceled.connect(print_event)

        # stop continuous transcription on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # start continuous speech recognition and write data to stream
        speech_recognizer.start_continuous_recognition()
        chunk = await file.read()
        stream.write(chunk)
        stream.close()

        # process data
        try:
            while not done or not recognized_queue.empty():
                # read from queue if not empty
                if not recognized_queue.empty():
                    item = await recognized_queue.get()
                    response = {
                        "text": item.result.text,
                        "reason": item.result.reason.name,
                    }
                    yield json.dumps(response)
                await asyncio.sleep(0.1)
        finally:
            # stop recognition and clean up
            logger.debug("Stopping recognition")
            await file.close()
            speech_recognizer.stop_continuous_recognition()
            # get remaining data
            if not recognized_queue.empty():
                item = await recognized_queue.get()
                response = {
                    "text": item.result.text,
                    "reason": item.result.reason.name,
                }
                yield json.dumps(response)
            logger.debug("Closed stream and stop recognition")

    # work in progress. Main problem right now: cannot send data directly in websocket
    # because callback functions cannot be async :(
    async def test_websocket(self, websocket: WebSocket):
        # get the correct audio format
        audio_format = AudioStreamFormat(
            channels=1,
            samples_per_second=16000,
            bits_per_sample=16,
        )
        # get the push stream
        stream = speechsdk.audio.PushAudioInputStream(audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        recognized_queue = asyncio.Queue()

        def recognized_callback(event):
            logger.info(f"RECOGNIZED: {event}")
            recognized_queue.put_nowait(event.result.text)

        speech_recognizer.recognized.connect(recognized_callback)
        speech_recognizer.recognizing.connect(
            lambda event: logger.debug(f"RECOGNIZING: {event}")
        )
        speech_recognizer.session_started.connect(
            lambda event: logger.info(f"SESSION STARTED: {event}")
        )
        speech_recognizer.session_stopped.connect(
            lambda event: logger.info(f"SESSION STOPPED {event}")
        )
        speech_recognizer.canceled.connect(
            lambda event: logger.info(f"CANCELED {event}")
        )

        # start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_bytes()
                stream.write(data)

                if not recognized_queue.empty():
                    item = await recognized_queue.get()
                    await websocket.send_text(item)
        except WebSocketDisconnect:
            logger.debug("Closing stream and stop recognition")
            stream.close()
            speech_recognizer.stop_continuous_recognition()
            logger.debug("Closed stream and stop recognition")
