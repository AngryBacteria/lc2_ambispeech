from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.utils.llm_util import LLMUtil, OpenaiModel

llmRouter = APIRouter(
    prefix="/api/llm",
    tags=["llm"],
)

llmUtil = LLMUtil()


@llmRouter.post("/hello/{model}")
async def hello(model: OpenaiModel):
    llmUtil.openai_model = model
    return await llmUtil.hello_chat_completion()


class Message(BaseModel):
    role: Literal['system', 'user']
    content: str


@llmRouter.post("/openai/{model}")
async def openai(model: OpenaiModel, messages: list[Message]):
    llmUtil.openai_model = model
    messages_list = [message.model_dump() for message in messages]
    return await llmUtil.chat_completion(messages_list)
