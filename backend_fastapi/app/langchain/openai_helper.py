from __future__ import annotations

import os
from enum import Enum

from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.schema.language_model import BaseLanguageModel
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict, List, Type

from app.utils.logging_util import logger


class OpenAIHelper:
    _instance = None
    llm: BaseLanguageModel = None
    config = None

    class OpenaiLangchainConfig(BaseModel):
        submodule: OpenAIModel = "gpt-4-32k"
        max_tokens: int = 20
        temperature: float = 1

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAIHelper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_API_KEY")
        else:
            self.config = OpenAIHelper.OpenaiLangchainConfig()
            self.llm = ChatOpenAI()
        logger.info("Created OpenAIHelper")
        self._initialized = True

    # TODO get_configurable_fields implementing

    def get_llm(self):
        return self.llm


class OpenAIModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
