from __future__ import annotations

import os
from enum import Enum

from langchain.chat_models import ChatOpenAI
from langchain.llms import LlamaCpp, OpenAI
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
from langchain.schema.language_model import BaseLanguageModel

from app.utils.openai_helper import OpenAIHelper


class LangchainUtil:
    """Singleton util class to handle various llm related operations with langchain"""

    _instance = None
    llm: BaseLanguageModel = None
    openai_helper = OpenAIHelper()

    # llama_helper = LlammaHelper()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LangchainUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        self.llm = ChatOpenAI()
        print("Created LangchainUtil")
        self._initialized = True

    async def hello_chat_completion(self):
        """Async Hello World chat completion example for openai"""
        response = self.llm.call("Hello World")
        return response

    async def chat_completion(self, model, message):
        helper = ModelHelperMapper.get_helper_for_model(model)
        if not helper:
            raise ValueError(f"Unsupported model: {model}")

        print(helper.get_config().model_dump())

        return self.llm.predict(message)

    def test(self):
        inputshema = self.llm.model_kwargs
        print(inputshema)
        return


class LLModel(str, Enum):
    """Enum for all supported Large Language models"""

    ChatOpenAI = "chat-open-ai"
    Llama = "llama-cpp"


class ModelHelperMapper:
    _mapping = {
        LLModel.ChatOpenAI: OpenAIHelper()
        # LLModel.Llama: LlamaHelper()
    }

    @classmethod
    def get_helper_for_model(cls, model: LLModel):
        return cls._mapping.get(model)
