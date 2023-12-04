from __future__ import annotations

import os
from enum import Enum
from typing import Literal

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel
from typing_extensions import TypedDict

from app.utils.logging_util import logger


class OpenAIUtil:
    """Singleton util class to handle various llm related operations with openai"""

    _instance = None
    openai_model: OpenaiModel = None
    client: OpenAI = None
    clientAsync: AsyncOpenAI = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAIUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        if os.getenv("OPENAI_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_KEY")
        else:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_KEY"),
            )
            self.clientAsync = AsyncOpenAI(
                api_key=os.getenv("OPENAI_KEY"),
            )
            self.openai_model = OpenaiModel.GPT_3_TURBO
        logger.info("Created OpenAIUtil")
        self._initialized = True

    async def hello_chat_completion(self, config: OpenaiCompletionConfig):
        """Async Hello World chat completion example for openai"""
        chat_completion = await self.clientAsync.chat.completions.create(
            messages=[{"role": "user", "content": "Hello world"}],
            model=self.openai_model.value,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p,
        )
        return chat_completion.choices[0].message.content

    async def chat_completion(self, messages, config: OpenaiCompletionConfig):
        """Async Non-Streaming OpenAI chat completion function"""
        chat_completion_resp = await self.clientAsync.chat.completions.create(
            model=self.openai_model.value,
            messages=messages,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p,
        )
        return chat_completion_resp.choices[0].message.content

    async def stream_chat_completion(self, messages, config: OpenaiCompletionConfig):
        """Async Streaming OpenAI chat completion function"""
        stream = await self.clientAsync.chat.completions.create(
            model=self.openai_model.value,
            messages=messages,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def get_embedding(self, text: str):
        """Calculates the embedding vector for a string input"""
        return (
            self.client.embeddings.create(input=[text], model="text-embedding-ada-002")
            .data[0]
            .embedding
        )

    async def get_embedding_async(self, text: str):
        """Calculates the embedding vector for a string input asynchronously"""
        emb = await self.clientAsync.embeddings.create(
            input=[text], model="text-embedding-ada-002"
        )
        return emb.data[0].embedding


class OpenaiCompletionConfig(BaseModel):
    frequency_penalty: float = 0
    max_tokens: int = 10
    presence_penalty: float = 0
    temperature: float = 1
    top_p: float = 1
    response_format: OpenaiResponseFormat = {"type": "text"}


class OpenaiResponseFormat(TypedDict):
    type: Literal["json_object", "text"]


class OpenaiCompletionBody(BaseModel):
    messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam]
    config: OpenaiCompletionConfig


class OpenaiModel(str, Enum):
    """Enum for all supported OpenAI models"""

    GPT_4_TURBO = "gpt-4-1106-preview"
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"
