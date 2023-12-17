from __future__ import annotations

import io
import os
from typing import Iterable, Union

import ctranslate2
from faster_whisper import WhisperModel, download_model
from faster_whisper.transcribe import TranscriptionInfo, Segment

from app.utils.logging_util import logger


class WhisperUtil:
    _instance = None
    model_size = "tiny"
    model_folder = "models"

    model_GPU: WhisperModel = None
    model_CPU: WhisperModel = None

    cpu_threads: int = None
    beam_size = 5
    useVad: bool = True
    useGPU: bool = True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WhisperUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_folder: str = "models"):
        if hasattr(self, "_initialized"):
            return

        # Check if the whisper models folder path exists
        self.model_folder = model_folder
        if not os.path.exists(os.path.join(self.model_folder)):
            raise EnvironmentError(
                f"Whisper models folder does not exist: {self.model_folder}"
            )

        # set amount of cpu cores to use
        cpu_count = os.cpu_count()
        self.cpu_threads = cpu_count if cpu_count and cpu_count > 0 else 4
        # download the model
        self.downloadModels()
        # Load the GPU model if supported
        if ctranslate2.get_cuda_device_count() >= 1 and self.useGPU:
            try:
                self.model_GPU = WhisperModel(
                    os.path.join(self.model_folder, self.model_size), device="cuda"
                )
                logger.debug("Created Whisper GPU-Model")
            except Exception as error:
                logger.error(f"GPU support for Whisper could not be loaded: {error}")
        # Load the CPU model
        try:
            self.model_CPU = WhisperModel(
                os.path.join(self.model_folder, self.model_size),
                device="cpu",
                cpu_threads=self.cpu_threads,
            )
            logger.debug("Created Whisper CPU-Model")
        except Exception as error:
            logger.error(f"GPU support for Whisper could not be loaded: {error}")
            if self.model_GPU is None:
                raise error

        logger.info(f"Created WhisperUtil [useVad={self.useVad}]")
        self._initialized = True

    def transcribe(self, data: bytes):
        segments: Union[None, Iterable[Segment]] = None
        info: Union[None, TranscriptionInfo] = None
        gpu_failed = True
        # Try to transcribe with GPU model
        if self.useGPU and self.model_GPU is not None:
            try:
                segments, info = self.model_GPU.transcribe(
                    io.BytesIO(data),
                    beam_size=self.beam_size,
                    vad_filter=self.useVad,
                )
                gpu_failed = False
                logger.debug(f"Inference with GPU")
            except Exception as e:
                logger.error(f"GPU model transcription failed: {e}")
                # Flag to indicate GPU failure, in case separate logic is needed
                gpu_failed = True
        # If GPU transcription failed or not available, try CPU model
        if gpu_failed:
            try:
                segments, info = self.model_CPU.transcribe(
                    io.BytesIO(data),
                    beam_size=self.beam_size,
                    vad_filter=self.useVad,
                )
                logger.debug(f"Inference with CPU")
            except Exception as e:
                logger.error(f"CPU model transcription also failed: {e}")
                raise e  # If both methods fail, re-raise the exception.

        if segments is None or info is None:
            raise Exception("Both GPU and CPU transcriptions failed.")
        logger.info(
            f"Starting inference: Detected language {info.language} with probability {info.language_probability}"
        )
        # VAD may reduce the audio length because of parts without speech
        logger.debug(f"Audio duration [{info.duration}][{info.duration_after_vad}]")
        for segment in segments:
            logger.debug(f"Recognized: {segment.text}")
            yield getattr(segment, "text", "")

        logger.info("Finished whisper audio-processing")

    def downloadModels(self):
        # Check if the model already exists. Download only if not
        potential_bin_path = os.path.join(
            self.model_folder, self.model_size, "model.bin"
        )
        if not os.path.exists(potential_bin_path):
            potential_model_path = os.path.join("models", self.model_size)
            os.makedirs(potential_model_path)
            path = download_model(self.model_size, potential_model_path)
            logger.info(f"Downloaded the Whisper model into: {path}")
