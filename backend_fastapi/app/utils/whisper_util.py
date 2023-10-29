from __future__ import annotations

import json
import logging
import multiprocessing

from pywhispercpp.model import Model

from app.utils.azure_util import AzureLanguageCode


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

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WhisperUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, language_code: AzureLanguageCode = AzureLanguageCode.DE_CH):
        self.language = language_code
        # set cpu cores to use
        cpu_count = multiprocessing.cpu_count()
        self.cpu_threads = cpu_count if cpu_count and cpu_count > 0 else 2

    # todo make yield return intermediate results with callback
    def transcribe_file(self, file_path: str, language: AzureLanguageCode):
        model = Model(
            "base",
            language=get_whisper_language(language),
            n_threads=self.cpu_threads,
            log_level=logging.INFO,
        )

        segments = model.transcribe(file_path, speed_up=True)
        for segment in segments:
            print(f"Analyzed Text: {segment.text}")
            response = {
                "text": segment.text,
                "reason": "Recognized",
            }
            yield json.dumps(response)
