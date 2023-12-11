import json
import os

from pydantic import BaseModel
from typing import List, Optional

class Symptom(BaseModel):
    symptom: str
    onset: str
    location: str
    context: str

class Medication(BaseModel):
    name: str
    dosage: str
    context: str

class Finding(BaseModel):
    finding: str
    context: str
    value: str

class Extraction(BaseModel):
    symptoms: List[Symptom]
    medications: List[Medication]
    findings: List[Finding]

class AudioData(BaseModel):
    folder: str
    name: str
    transcript: str
    synthetic: bool
    noise: bool
    extraction: Optional[Extraction] = None


dir_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(dir_path, "lc2_data.json")

with open(json_file_path, "r", encoding="utf-8") as file:
    nlp_data = json.load(file)

    audio_data_list = []
    for item in nlp_data.get("files", []):
        audio_data = AudioData(**item)

        if audio_data.extraction is not None:
            print(audio_data.extraction.symptoms[0])

        audio_data_list.append(audio_data)
        