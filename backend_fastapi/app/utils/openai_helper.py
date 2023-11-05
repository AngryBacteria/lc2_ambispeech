from __future__ import annotations

import os
from enum import Enum

from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from dotenv import load_dotenv
from pydantic import BaseModel


class OpenAIHelper:
    """Singleton util class to handle various llm related operations with langchain"""

    _instance = None
    config = None

    class OpenaiCompletionConfig(BaseModel):
        submodel: OpenAIModel = "gpt-3.5-turbo"
        max_tokens: int = 10


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAIHelper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        if os.getenv("OPENAI_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_KEY")
        else:
            self.config = OpenAIHelper.OpenaiCompletionConfig()
        print("Created OpenAIHelper")
        self._initialized = True

    def get_config(self):
        return self.config


class OpenAIModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
