from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.utils.openai_util import (
    OpenAIUtil,
    OpenaiModel,
    OpenaiCompletionConfig,
    OpenaiCompletionBody,
)

llmRouter = APIRouter(
    prefix="/api/llm",
    tags=["llm"],
)

llmUtil = OpenAIUtil()


@llmRouter.post("/hello/{model}")
async def hello(model: OpenaiModel, config: OpenaiCompletionConfig):
    """Hello World example for large language models"""
    llmUtil.openai_model = model
    return await llmUtil.hello_chat_completion(config)


@llmRouter.post("/openai/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    """Non-Streaming OpenAI chat completion"""
    llmUtil.openai_model = model
    return await llmUtil.chat_completion(body.messages, body.config)


@llmRouter.post("/openaistream/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    """Streaming OpenAI chat completion"""
    llmUtil.openai_model = model
    return StreamingResponse(
        llmUtil.stream_chat_completion(body.messages, body.config),
        media_type="text/event-stream",
    )
