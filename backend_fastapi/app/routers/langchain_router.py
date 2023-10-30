from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.utils.langchain_util import LangchainUtil, OpenAIModel

langchainRouter = APIRouter(
    prefix="/api/langchain",
    tags=["langchain"],
)

langchainUtil = LangchainUtil()


class OpenaiCompletionMessage(BaseModel):
    role: Literal["system", "user"]
    content: str


class OpenaiCompletionConfig(BaseModel):
    frequency_penalty: float = 0
    max_tokens: int = 10
    presence_penalty: float = 0
    temperature: float = 1
    top_p: float = 1


class OpenaiCompletionBody(BaseModel):
    messages: list[OpenaiCompletionMessage]
    config: OpenaiCompletionConfig


@langchainRouter.post("/hello/")
async def hello():
    """Hello World example for large language models"""
    return await langchainUtil.hello_chat_completion()


@langchainRouter.post("/openai/{model}")
async def openai(model: OpenAIModel, body: OpenaiCompletionBody):
    """Non-Streaming OpenAI chat completion"""
    messages_list = [message.model_dump() for message in body.messages]
    return await langchainUtil.chat_completion(model, messages_list, body.config)


# TODO under Construction
@langchainRouter.post("llamacpp/")
async def llama():
    return
