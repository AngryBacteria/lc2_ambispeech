from __future__ import annotations

import os
from enum import Enum

from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from dotenv import load_dotenv


class LangchainUtil:
    """Singleton util class to handle various llm related operations with langchain"""

    _instance = None
    llm: BaseChatModel = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LangchainUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        if os.getenv("OPENAI_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_KEY")
        else:
            self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        print("Created LangchainUtil")
        self._initialized = True

    async def hello_chat_completion(self):
        """Async Hello World chat completion example for openai"""
        response = self.llm.call("Hello World")

        return response

    async def chat_completion(self, model, messages_list, config):
        return self.llm._identifying_params


class OpenAIModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
