from __future__ import annotations

import asyncio
import os
from enum import Enum
import queue
from time import sleep

from azure.cognitiveservices.speech import SpeechConfig
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioStreamFormat
from dotenv import load_dotenv
from fastapi import UploadFile

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

    def speech_recognition_with_push_stream(self, file: UploadFile, params):
        """Azure continuous recognition for a SpooledFile"""
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

        # recognize callback
        recognized_queue = queue.Queue()
        done = False

        def recognized_callback(evt):
            logger.info(f"RECOGNIZED: {evt}")
            recognized_queue.put_nowait(evt)

        # connect callbacks
        speech_recognizer.recognizing.connect(
            lambda evt: logger.debug(f"RECOGNIZING: {evt}")
        )
        speech_recognizer.recognized.connect(recognized_callback)
        speech_recognizer.session_started.connect(
            lambda evt: logger.info(f"SESSION STARTED: {evt}")
        )
        speech_recognizer.session_stopped.connect(
            lambda evt: logger.info(f"SESSION STOPPED {evt}")
        )
        speech_recognizer.canceled.connect(lambda evt: logger.info(f"CANCELED {evt}"))

        # The buffer size
        n_bytes = 4096

        # start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # start pushing data until all data has been read from the file and the queue is empty
        try:
            while not done or not recognized_queue.empty():
                # check if there are still bytes left
                chunk = file.file.read(n_bytes)
                logger.debug("read {} bytes".format(len(chunk)))
                if not chunk:
                    done = True
                else:
                    stream.write(chunk)

                # read from queue if not empty
                if not recognized_queue.empty():
                    item = recognized_queue.get()
                    yield f"{item.result.text}"
                sleep(0.1)
        finally:
            # stop recognition and clean up
            file.file.close()
            stream.close()
            speech_recognizer.stop_continuous_recognition()
            # get latest data
            if not recognized_queue.empty():
                item = recognized_queue.get()
                yield f"{item.result.text}"
