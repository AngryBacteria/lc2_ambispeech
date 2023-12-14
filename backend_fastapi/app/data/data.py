import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Literal, Union

from langchain_core.language_models import BaseLLM, BaseChatModel
from pydantic import BaseModel


# Audio File data models
class Symptom(BaseModel):
    """Class for the data of a symptom"""

    symptom: str
    onset: str
    location: str
    context: str


class Medication(BaseModel):
    """Class for the data of a medication"""

    name: str
    dosage: str
    context: str


class Finding(BaseModel):
    """Class for the data of a finding"""

    finding: str
    context: str
    value: str


class Extraction(BaseModel):
    """Class for the data of the extraction"""

    symptoms: List[Symptom]
    medications: List[Medication]
    findings: List[Finding]


class AudioData(BaseModel):
    """Class for the data of the audio files. Includes the optional extraction data."""

    folder: str
    name: str
    transcript: str
    synthetic: bool
    noise: bool
    extraction: Optional[Extraction] = None


# LLM data models
class GenericMessage(BaseModel):
    """Generic message for prompting llm models"""

    content: str
    role: Literal["user", "system"]


class GenericPrompt(BaseModel):
    """Generic prompt for prompting llm models"""

    messages: List[GenericMessage]
    placeholder_index: int


class PromptData(BaseModel):
    """Prompt data that is available in the json file"""

    prompts: List[GenericPrompt]
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


class GenericLangChainModel(ABC):
    """Interface for all of our supported langchain models"""

    @abstractmethod
    def get_llm(self) -> Union[BaseChatModel, BaseLLM]:
        pass


class LLMService(str, Enum):
    """All supported langchain services"""

    OPENAI = "openai"
    GPT4ALL = "gpt4all"


_dir_path = os.path.dirname(os.path.realpath(__file__))
_json_file_path = os.path.join(_dir_path, "lc2_data.json")
"""Parses the data from the json file and makes it available in the whole app"""
with open(_json_file_path, "r", encoding="utf-8") as file:
    _nlp_data = json.load(file)

    # parse audio data
    audio_file_data = []
    for _item in _nlp_data.get("files", []):
        _audio_data = AudioData(**_item)
        audio_file_data.append(_audio_data)

    # parse prompt data
    prompt_data = PromptData(**_nlp_data["prompting"])
