from __future__ import annotations

import os
from enum import Enum

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from app.utils.openai_helper import OpenAIHelper

from dotenv import load_dotenv

from app.utils.logging_util import logger


class LangchainUtil:
    """Singleton util class to handle various llm related operations with langchain"""

    _instance = None
    prompt_template = PromptTemplate(
        input_variables=["transcript"],
        template="""Gegeben ist das folgende Transkript eines Dialogs zwischen Ärzten und Patienten. Bitte extrahiere 
        spezifische Informationen über Symptome und Medikamente und gib diese im JSON-Format zurück:

           {transcript}
            
            Bitte geben Sie das Ergebnis im folgenden Format: 
            
            „Symptome“: [„Symptom1“, „Symptom2“, …],
            „Medikamente“: [„Medikament1“, „Medikament2“, …]
             """,
    )

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LangchainUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        logger.info("Created LangchainUtil")
        self._initialized = True

    # does not work anymore
    async def hello_chat_completion(self):
        """Async Hello World chat completion example for openai"""
        response = (
            ModelHelperMapper.get_helper_for_model(LLModel.ChatOpenAI)
            .get_llm()
            .call("Hello World")
        )
        return response

    async def chat_completion(self, model, transcript):
        helper = ModelHelperMapper.get_helper_for_model(model)
        if not helper:
            raise ValueError(f"Unsupported model: {model}")

        chain = LLMChain(llm=helper.get_llm(), prompt=self.prompt_template)

        return chain.run(transcript)

    async def test(self):
        return ModelHelperMapper.get_helper_for_model(LLModel.ChatOpenAI)


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
