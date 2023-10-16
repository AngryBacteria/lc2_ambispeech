from __future__ import annotations

import os
from enum import Enum

import openai
from dotenv import load_dotenv


class LLMUtil:
    """Singleton util class to handle various llm related operations"""
    _instance = None
    openai_model: OpenaiModel = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LLMUtil, cls).__new__(cls)
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
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            presence_penalty=config.presence_penalty
        )
        return chat_completion_resp.choices[0].message.content

    async def chat_completion(self, messages, config):
        """Async Non-Streaming OpenAI chat completion function"""
        chat_completion_resp = await openai.ChatCompletion.acreate(
            model=self.openai_model.value,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            presence_penalty=config.presence_penalty
        )
        return chat_completion_resp.choices[0].message.content

    async def stream_chat_completion(self, messages, config):
        """Async Streaming OpenAI chat completion function"""
        chat_completion_resp = await openai.ChatCompletion.acreate(
            model=self.openai_model.value,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            presence_penalty=config.presence_penalty,
            stream=True
        )
        async for chunk in chat_completion_resp:
            text = chunk['choices'][0].get('delta').get('content')
            if text is not None:
                yield chunk['choices'][0]['delta'].get('content')


class OpenaiModel(str, Enum):
    """Enum for all supported OpenAI models"""
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
