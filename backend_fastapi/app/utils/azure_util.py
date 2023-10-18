from __future__ import annotations

import asyncio
import os
from enum import Enum
import queue
from time import sleep
from typing import IO
from wave import _wave_params

from azure.cognitiveservices.speech import SpeechConfig
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioStreamFormat
from dotenv import load_dotenv
from fastapi import UploadFile


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

    def azure_long_s2t(self, file_path: str):
        """Azure continuous recognition for an existing audio file"""
        done = False
        chunks = queue.Queue()
        audio_config = speechsdk.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        def stop_recognition(event):
            """Stop recognition event"""
            print(f"CLOSING on: {event}")
            speech_recognizer.stop_continuous_recognition_async()
            nonlocal done
            done = True

        def on_recognized(event):
            """Sentence got recognized event"""
            print(f"RECOGNIZED: {event}")
            chunks.put_nowait(event)

        #speech_recognizer.recognizing.connect(
        #    lambda event: print(f"RECOGNIZING: {event}")
        #)
        speech_recognizer.recognized.connect(on_recognized)
        speech_recognizer.session_started.connect(
            lambda event: print(f"SESSION STARTED: {event}")
        )
        speech_recognizer.session_stopped.connect(
            lambda event: print(f"SESSION STOPPED: {event}")
        )
        speech_recognizer.canceled.connect(lambda evt: print(f"CANCELED: {evt}"))

        speech_recognizer.session_stopped.connect(stop_recognition)
        speech_recognizer.canceled.connect(stop_recognition)

        speech_recognizer.start_continuous_recognition()

        while not done or not chunks.empty():
            if not chunks.empty():
                item = chunks.get()
                yield f"{item.result.text}"
            else:
                sleep(1)

        print("DONE WITH SPEECH RECOGNITION")

    def speech_recognition_with_push_stream(self, file: UploadFile, params):
        # get the correct audio format
        audio_format = AudioStreamFormat(
            channels=params.nchannels,
            samples_per_second=params.framerate,
            bits_per_sample=params.sampwidth * 8
        )
        # get the push stream
        stream = speechsdk.audio.PushAudioInputStream(audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        #recognize callback
        def recognized_callback(evt):
            print(f'RECOGNIZED: {evt}')

        # connect callbacks
        speech_recognizer.recognizing.connect(lambda evt: print(f'RECOGNIZING: {evt}'))
        speech_recognizer.recognized.connect(recognized_callback)
        speech_recognizer.session_started.connect(lambda evt: print(f'SESSION STARTED: {evt}'))
        speech_recognizer.session_stopped.connect(lambda evt: print(f'SESSION STOPPED {evt}'))
        speech_recognizer.canceled.connect(lambda evt: print(f'CANCELED {evt}'))

        # The buffer size
        n_bytes = 4096

        # start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # start pushing data until all data has been read from the file
        try:
            while True:
                chunk = file.file.read(n_bytes)
                print('read {} bytes'.format(len(chunk)))
                if not chunk:
                    break

                stream.write(chunk)
                sleep(.1)
        finally:
            # stop recognition and clean up
            file.file.close()
            stream.close()
            speech_recognizer.stop_continuous_recognition()