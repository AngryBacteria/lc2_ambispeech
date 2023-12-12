import json
import os
from enum import Enum
from typing import List, Optional, Literal

from pydantic import BaseModel


# Audio File data models
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


# LLM data models
class LLMBaseMessage(BaseModel):
    content: str
    role: Literal["user", "system"]


class BasePrompt(BaseModel):
    messages: List[LLMBaseMessage]
    placeholder_index: int


class PromptData(BaseModel):
    prompts: List[BasePrompt]
    userinput_placeholder: str
    jsonexample_placeholder: str
    textexample_placeholder: str


# "Interfaces" that can be used in the whole app
class OpenaiModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4_TURBO = "gpt-4-1106-preview"  # newest gpt 4 turbo model (supports json mode, huge context size)
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"  # gpt 4 model with context size of 32k tokens
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
    GPT_3_TURBO_1106 = "gpt-3.5-turbo-1106"  # newest gpt 3.5 model (supports json_mode)


_dir_path = os.path.dirname(os.path.realpath(__file__))
_json_file_path = os.path.join(_dir_path, "lc2_data.json")
with open(_json_file_path, "r", encoding="utf-8") as file:
    _nlp_data = json.load(file)

    # parse audio data
    audio_file_data = []
    for _item in _nlp_data.get("files", []):
        _audio_data = AudioData(**_item)
        audio_file_data.append(_audio_data)

    # parse prompt data
    prompt_data = PromptData(**_nlp_data["prompting"])
