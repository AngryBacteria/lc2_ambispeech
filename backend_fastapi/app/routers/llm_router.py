from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel

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
async def hello(model: OpenaiModel):
    llmUtil.openai_model = model
    return await llmUtil.hello_chat_completion()


@llmRouter.post("/openai/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    llmUtil.openai_model = model
    print(body.config)
    messages_list = [message.model_dump() for message in body.messages]
    return await llmUtil.chat_completion(messages_list, body.config)
