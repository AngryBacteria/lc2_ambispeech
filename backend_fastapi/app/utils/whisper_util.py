from __future__ import annotations

import json
import os

import ctranslate2
from faster_whisper import WhisperModel

from app.utils.azure_util import AzureLanguageCode
from app.utils.logging_util import logger


def get_whisper_language(language: AzureLanguageCode):
    match language:
        case AzureLanguageCode.DE_CH:
            return "de"
        case AzureLanguageCode.DE_AT:
            return "de"
        case AzureLanguageCode.DE_DE:
            return "de"
        case AzureLanguageCode.EN_GB:
            return "en"
        case AzureLanguageCode.EN_US:
            return "en"
        case _:
            return "de"


class WhisperUtil:
    _instance = None
    language: AzureLanguageCode = None
    cpu_threads: int = None
    # whisper config
    model_size = "base"
    model: WhisperModel = None
    beam_size = 5
    useVad: bool = True
    useGPU: bool = True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WhisperUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, language_code: AzureLanguageCode = AzureLanguageCode.DE_CH):
        if hasattr(self, "_initialized"):
            return
        self.language = language_code
        # set cpu cores to use
        cpu_count = os.cpu_count()
        self.cpu_threads = cpu_count if cpu_count and cpu_count > 0 else 4

        if ctranslate2.get_cuda_device_count() >= 1 and self.useGPU:
            try:
                self.model = WhisperModel(self.model_size, device="cuda")
            except Exception as error:
                logger.error(f"Cuda could not be loaded: {error}")
            finally:
                logger.info("Created WhisperUtil [GPU support]")
        else:
            self.model = WhisperModel(
                self.model_size, device="cpu", cpu_threads=self.cpu_threads
            )
            logger.info("Created WhisperUtil [CPU support]")

        self._initialized = True

    def transcribe_file(self, file_path: str, language_code: AzureLanguageCode = None):
        segments, info = self.model.transcribe(
            file_path,
            beam_size=self.beam_size,
            vad_filter=self.useVad,
            language=get_whisper_language(language_code),
        )
        logger.info(
            f"Detected language {info.language} with probability {info.language_probability}"
        )
        logger.info(f"Audio duration [{info.duration}][{info.duration_after_vad}]")

        for segment in segments:
            logger.debug(f"Recognized: {segment.text}")
            yield getattr(segment, 'text', '')

        logger.info("Finished whisper audio-processing")
