import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Literal, Union
from typing_extensions import TypedDict

import pandas
from anyio import Lock
from langchain_core.language_models import BaseLLM, BaseChatModel
from pydantic import BaseModel


# Audio File data models
class Symptom(BaseModel):
    """Class for the data of a symptom"""

    symptom: str
    onset: str
    location: str
    context: str


class Extraction(BaseModel):
    """Class for the data of the extraction"""

    symptoms: List[Symptom]


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


# OpenAI data models
class OpenaiModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4_TURBO = "gpt-4-1106-preview"  # newest gpt 4 turbo model (supports json mode, huge context size)
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"  # gpt 4 model with context size of 32k tokens
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
    GPT_3_TURBO_1106 = "gpt-3.5-turbo-1106"  # newest gpt 3.5 model (supports json_mode)


class OpenaiResponseFormat(TypedDict):
    """Response format for openai chat completion requests. The newest models support JSON"""

    type: Literal["json_object", "text"]


class OpenaiCompletionConfig(BaseModel):
    """Config object for openai chat completion requests"""

    frequency_penalty: float = 0
    max_tokens: int = 10
    presence_penalty: float = 0
    temperature: float = 1
    top_p: float = 1
    response_format: OpenaiResponseFormat = {"type": "text"}


# Language Chain data models
class GenericLangChainModel(ABC):
    """Interface for all of our supported langchain models"""

    @abstractmethod
    def get_llm(self) -> Union[BaseChatModel, BaseLLM]:
        pass


class LLMService(str, Enum):
    """All supported langchain services"""

    OPENAI = "openai"
    GPT4ALL = "gpt4all"


class AzureLanguageCode(str, Enum):
    """Enum for all supported languages (Azure)"""

    DE_CH = "de-CH"
    DE_DE = "de-DE"
    DE_AT = "de-AT"
    EN_GB = "en-GB"
    EN_US = "en-US"


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

# Lock for operations on the data in this file and in the catalogs folder
lock = Lock()


def transform_icd10_csv(only_r: bool = True):
    """Transforms the icd10 csv file into a pandas dataframe and
    removes all rows that contain "Nicht belegte Schlüsselnummer"""
    column_names = [
        "klassifikationsebene",
        "schlüsselnummer_ort",
        "vier_fuenfsteller_art",
        "kapitelnummer",
        "erster_dreisteller",
        "schlüsselnummer_ohne_kreuz",
        "schlüsselnummer_mit_punkt",
        "schlüsselnummer",
        "klassentitel",
        "dreisteller_titel",
        "viersteller_titel",
        "fuenfsteller_titel",
        "schlüsselnummer_verwendung_paragraph295",
        "schlüsselnummer_verwendung_paragraph301",
        "mortalitätsliste1_bezug",
        "mortalitätsliste2_bezug",
        "mortalitätsliste3_bezug",
        "mortalitätsliste4_bezug",
        "morbiditätsliste_bezug",
        "geschlechtsbezug_schlüsselnummer",
        "fehler_geschlechtsbezug",
        "untere_altersgrenze",
        "obere_altersgrenze",
        "fehler_altersbezug",
        "seltenheit_mitteleuropa",
        "schlüsselnummer_inhalt_belegt",
        "ifsg_meldung",
        "ifsg_labor",
    ]
    column_types = {
        "klassifikationsebene": str,
        "schlüsselnummer_ort": str,
        "vier_fuenfsteller_art": str,
        "kapitelnummer": str,
        "erster_dreisteller": str,
        "schlüsselnummer_ohne_kreuz": str,
        "schlüsselnummer_mit_punkt": str,
        "schlüsselnummer": str,
        "klassentitel": str,
        "dreisteller_titel": str,
        "viersteller_titel": str,
        "fuenfsteller_titel": str,
        "schlüsselnummer_verwendung_paragraph295": str,
        "schlüsselnummer_verwendung_paragraph301": str,
        "mortalitätsliste1_bezug": str,
        "mortalitätsliste2_bezug": str,
        "mortalitätsliste3_bezug": str,
        "mortalitätsliste4_bezug": str,
        "morbiditätsliste_bezug": str,
        "geschlechtsbezug_schlüsselnummer": str,
        "fehler_geschlechtsbezug": str,
        "untere_altersgrenze": str,
        "obere_altersgrenze": str,
        "fehler_altersbezug": str,
        "seltenheit_mitteleuropa": str,
        "schlüsselnummer_inhalt_belegt": str,
        "ifsg_meldung": str,
        "ifsg_labor": str,
    }
    df = pandas.read_csv(
        "catalogs/icd10gm.txt", sep=";", names=column_names, dtype=column_types
    )

    # remove rows that contain "Nicht belegte Schlüsselnummer"
    df = df[
        ~df["klassentitel"].str.contains(
            "Nicht belegte Schlüsselnummer", na=False, case=False
        )
    ]

    if only_r:
        # remove all rows that are not in the category R
        df = df[df["erster_dreisteller"].str.contains("R", na=False, case=False)]

    return df
