import asyncio
import os
import time
import wave

import pandas as pd

from app.data.audio_files import medical_texts
from app.utils.azure_util import AzureUtil
from app.utils.general_util import get_wer
from app.utils.logging_util import logger
from app.utils.whisper_util import WhisperUtil

file_base_path = "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\testfiles"
excel_path = "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\LC2_Resultate_S2T.xlsx"
service = "azure"


# helper function for later
async def transcribe_audio_with_azure(azure: AzureUtil, _data, _audio_params):
    return "".join(
        [
            text
            async for text in azure.transcribe_with_push_stream(
                _data, _audio_params, use_diarization=False
            )
        ]
    )


def test_all_files(save_to_excel: bool = True, only_one_file: bool = False):
    whisper = None
    azure = None
    # init whisper
    if service == "whisper":
        whisper = WhisperUtil()
        test_file_path = "C:\\Users\\nicog\\Downloads\\whatstheweatherlike.wav"
        # let it run once, that way the models are loaded into memory
        with open(test_file_path, "rb") as file:
            data = file.read()
            "".join(whisper.transcribe(data))

        if whisper.useGPU:
            cpu = ""
            gpu = "RTX407OTI"
        else:
            cpu = "Ryzen 7 5800x"
            gpu = ""

        model = whisper.model_size
        library = "faster-whisper"
        params = f"beam_size={whisper.beam_size}, float16"
    # azure init
    else:
        azure = AzureUtil()
        model = "azure"
        library = "azure python sdk"
        params = ""
        cpu = "Ryzen 7 5800x"
        gpu = "RTX4070 TI"

    # set logging level
    logger.setLevel("ERROR")
    # Check if the Excel file exists, if so, use it, else create a new DataFrame
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
    else:
        df = pd.DataFrame(
            columns=[
                "model",
                "library",
                "cpu",
                "gpu",
                "params",
                "audio_wav",
                "synthetic",
                "noise",
                "exec_time",
                "length",
                "wer",
                "mer",
                "wil",
                "wip",
                "output",
            ]
        )

    # iterate over all files
    for test_file in medical_texts["files"]:
        audio_wav_path = os.path.join(
            file_base_path, test_file["folder"], test_file["name"]
        )

        with open(audio_wav_path, "rb") as file:
            data = file.read()

        with wave.open(audio_wav_path, "rb") as audio_file:
            audio_params = audio_file.getparams()

        # transcribe audiofile
        start_time = time.time()
        if service == "whisper":
            output = "".join(whisper.transcribe(data))
        else:
            output = asyncio.run(transcribe_audio_with_azure(azure, data, audio_params))
        end_time = time.time()

        # calculate data
        length = len(output)
        report = get_wer(test_file["transcript"], output)
        exec_time = (end_time - start_time) * 1000

        new_row = [
            model,
            library,
            cpu,
            gpu,
            params,
            test_file["name"],
            test_file["synthetic"],
            test_file["noise"],
            round(exec_time),
            length,
            report.get("wer"),
            report.get("mer"),
            report.get("wil"),
            report.get("wip"),
            output,
        ]
        df.loc[len(df)] = new_row

        if only_one_file:
            break

    # save to excel
    if save_to_excel:
        df.to_excel(excel_path, "data", index=False)


test_all_files(True, False)
