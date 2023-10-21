from __future__ import annotations

import os
from enum import Enum

import openai
from dotenv import load_dotenv


class OpenAIUtil:
    """Singleton util class to handle various llm related operations with openai"""

    _instance = None
    openai_model: OpenaiModel = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAIUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        if os.getenv("OPENAI_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_KEY")
        else:
            openai.api_key = os.getenv("OPENAI_KEY")
            self.openai_model = OpenaiModel.GPT_3_TURBO

    async def hello_chat_completion(self, config):
        """Async Hello World chat completion example for openai"""
        chat_completion_resp = await openai.ChatCompletion.acreate(
            model=self.openai_model.value,
            messages=[{"role": "user", "content": "Hello world"}],
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p
        )
        return chat_completion_resp.choices[0].get("message").get("content")

    async def chat_completion(self, messages, config):
        """Async Non-Streaming OpenAI chat completion function"""
        chat_completion_resp = await openai.ChatCompletion.acreate(
            model=self.openai_model.value,
            messages=messages,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p
        )
        return chat_completion_resp.choices[0].get("message").get("content")

    async def stream_chat_completion(self, messages, config):
        """Async Streaming OpenAI chat completion function"""
        chat_completion_resp = await openai.ChatCompletion.acreate(
            model=self.openai_model.value,
            messages=messages,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p,
            stream=True,
        )
        async for chunk in chat_completion_resp:
            text = chunk["choices"][0].get("delta").get("content")
            if text is not None:
                yield text


class OpenaiModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
