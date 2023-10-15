import os

from azure.cognitiveservices.speech import SpeechConfig
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv


class SpeechUtil(object):
    _instance = None
    speech_config: SpeechConfig
    azure_region: str
    azure_speech_Key: str
    language_code: str

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpeechUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, language_code: str = "de-DE"):
        load_dotenv()
        if os.getenv("AZURE_REGION") is None or os.getenv("AZURE_SPEECH_RESOURCE_KEY") is None:
            raise EnvironmentError(".env file is missing the AZURE_SPEECH_RESOURCE_KEY or AZURE_REGION")
        else:
            self.azure_region = os.getenv("AZURE_REGION")
            self.azure_speech_Key = os.getenv("AZURE_SPEECH_RESOURCE_KEY")
            self.language_code = language_code

            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_Key,
                region=self.azure_region,
                speech_recognition_language=self.language_code
            )

    def file_s2t(self, file_path):
        audio_config = speechsdk.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once_async().get()
        return result
