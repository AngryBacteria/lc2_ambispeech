from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel

from app.data.data import OpenaiModel
from app.utils.langchain_util import GenericLangChainModel
from app.utils.logging_util import logger


class OpenAIHelper(GenericLangChainModel):
    _instance = None
    llm: BaseLanguageModel = None

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
            self.llm = ChatOpenAI(model=OpenaiModel.GPT_4_TURBO)
        logger.info("Created OpenAIHelper")
        self._initialized = True

    # TODO get_configurable_fields implementing

    def get_llm(self):
        return self.llm
