from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.utils.llm_util import LLMUtil, OpenaiModel

llmRouter = APIRouter(
    prefix="/api/llm",
    tags=["llm"],
)

llmUtil = LLMUtil()


class OpenaiCompletionMessage(BaseModel):
    role: Literal['system', 'user']
    content: str


class OpenaiCompletionConfig(BaseModel):
    max_tokens: int = 10
    temperature: float = 1
    presence_penalty: float = 0
    top_p: float = 1


class OpenaiCompletionBody(BaseModel):
    messages: list[OpenaiCompletionMessage]
    config: OpenaiCompletionConfig


@llmRouter.post("/hello/{model}")
async def hello(model: OpenaiModel, config: OpenaiCompletionConfig):
    llmUtil.openai_model = model
    return await llmUtil.hello_chat_completion(config)


@llmRouter.post("/openai/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    llmUtil.openai_model = model
    messages_list = [message.model_dump() for message in body.messages]
    return await llmUtil.chat_completion(messages_list, body.config)


@llmRouter.post("/openaistream/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    llmUtil.openai_model = model
    messages_list = [message.model_dump() for message in body.messages]
    return StreamingResponse(llmUtil.stream_chat_completion(messages_list, body.config), media_type='text/event-stream')
