from __future__ import annotations

import os
from enum import Enum

from langchain.llms import OpenAI
from dotenv import load_dotenv


class LangchainUtil:
    """Singleton util class to handle various llm related operations with langchain"""

    _instance = None
    #TODO interrchangeable llms
    llm = OpenAI(open_api_key=os.getenv("OPENAI_KEY"))

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LangchainUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        if os.getenv("OPENAI_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_KEY")
        else:
            llm = OpenAI()

    async def hello_chat_completion(self):
        """Async Hello World chat completion example for openai"""
        response = self.llm.predict("Hello World")

        return response
