from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel

from app.data.data import OpenaiModel, OpenaiCompletionConfig
from app.utils.logging_util import logger


class OpenAIUtil:
    """Singleton util class to handle various llm related operations with openai"""

    _instance = None
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
        if os.getenv("OPENAI_API_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_API_KEY")
        else:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
            )
            self.clientAsync = AsyncOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        logger.info("Created OpenAIUtil")
        self._initialized = True

    async def hello_chat_completion(
        self, config: OpenaiCompletionConfig, model: OpenaiModel
    ):
        """Async Hello World chat completion example for openai"""
        chat_completion = await self.clientAsync.chat.completions.create(
            messages=[{"role": "user", "content": "Hello world"}],
            model=model,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p,
        )
        logger.debug(
            f"""Prompt Token [{chat_completion.usage.prompt_tokens}]
            Completion Tokens [{chat_completion.usage.completion_tokens}]
            Total Tokens [{chat_completion.usage.total_tokens}]"""
        )
        return chat_completion.choices[0].message.content

    async def chat_completion(
        self, messages, config: OpenaiCompletionConfig, model: OpenaiModel
    ):
        """Async Non-Streaming OpenAI chat completion function"""
        chat_completion_resp = await self.clientAsync.chat.completions.create(
            model=model,
            messages=messages,
            frequency_penalty=config.frequency_penalty,
            max_tokens=config.max_tokens,
            presence_penalty=config.presence_penalty,
            temperature=config.temperature,
            top_p=config.top_p,
        )
        return chat_completion_resp.choices[0].message.content

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


# todo: replace by GenericMessage Interface
class OpenaiCompletionBody(BaseModel):
    """Body to pass in FastAPI router when handling openai requests"""

    messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam]
    config: OpenaiCompletionConfig
