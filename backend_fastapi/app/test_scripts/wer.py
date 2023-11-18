import os
import time

import pandas as pd

from app.model.references import medical_texts
from app.utils.general_util import getWER
from app.utils.logging_util import logger
from app.utils.whisper_util import WhisperUtil

# set logging level to info
logger.setLevel("INFO")

# whisper init
whisper = WhisperUtil()
test_file_path = "C:\\Users\\nicog\\Downloads\\whatstheweatherlike.wav"
# let it run once, that way the models are loaded into memory
with open(test_file_path, "rb") as file:
    data = file.read()
    "".join(whisper.transcribe(data))

# constants
audio_wav_paths = [
    "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\Testfiles\\Ohne Hintergrundgeräusche\\dialog-herzinfarkt (ohne).wav",
    "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\Testfiles\\Ohne Hintergrundgeräusche\\dialog-appendizitis (ohne).wav",
    "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\Testfiles\\Mit Hintergrundgeräuschen\\dialog-herzinfarkt (mit).wav",
    "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\Testfiles\\Mit Hintergrundgeräuschen\\dialog-appendizitis (mit).wav",
]
excel_path = "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\LC2_Resultate_S2T.xlsx"
model = whisper.model_size
library = "faster-whisper"
cpu = "Ryzen 7 5800x"
gpu = "RTX407OTI"
params = f"beam_size={whisper.beam_size}, float16"

# todo: read from existing not overwrite
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
            "exec_time",
            "length",
            "wer",
            "mer",
            "wil",
            "output",
        ]
    )

# iterate over all files
for audio_wav_path in audio_wav_paths:
    audio_wav = audio_wav_path.split("\\")[-1]

    with open(audio_wav_path, "rb") as file:
        data = file.read()

    # transcribe audiofile
    start_time = time.time()
    output = "".join(whisper.transcribe(data))
    end_time = time.time()

    # get reference data
    # todo somehow make this better (what if more audio files get added)
    reference = (
        medical_texts["herzinfarkt"]
        if "herzinfarkt" in audio_wav
        else medical_texts["appendizitis"]
    )

    # calculate data
    length = len(output)
    report = getWER(reference, output)
    exec_time = (end_time - start_time) * 1000

    # add new row
    if whisper.useGPU:
        cpu = ""
    else:
        gpu = ""
    new_row = [
        model,
        library,
        cpu,
        gpu,
        params,
        audio_wav,
        round(exec_time),
        length,
        report.get("wer"),
        report.get("mer"),
        report.get("wil"),
        output,
    ]
    df.loc[len(df)] = new_row


# save to excel
df.to_excel(excel_path, "data", index=False)
