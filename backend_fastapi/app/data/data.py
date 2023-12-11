import json
import os
from typing import List, Optional, Literal

from pydantic import BaseModel


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


class LLMBaseMessage(BaseModel):
    content: str
    role: Literal["user", "system"]


class BasePrompt(BaseModel):
    messages: List[LLMBaseMessage]
    placeholder_index: int


# TODO: Replace llm prompt with
_dir_path = os.path.dirname(os.path.realpath(__file__))
_json_file_path = os.path.join(_dir_path, "lc2_data.json")
with open(_json_file_path, "r", encoding="utf-8") as file:
    nlp_data = json.load(file)

    # parse audio data
    audio_file_data = []
    for item in nlp_data.get("files", []):
        audio_data = AudioData(**item)
        audio_file_data.append(audio_data)

    # parse prompt data
    llm_prompts = []
    for prompt in nlp_data["prompting"].get("prompts", []):
        base_prompt = BasePrompt(**prompt)
        llm_prompts.append(base_prompt)
