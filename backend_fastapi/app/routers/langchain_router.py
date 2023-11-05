from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel

from app.utils.langchain_util import LangchainUtil, LLModel

langchainRouter = APIRouter(
    prefix="/api/langchain",
    tags=["langchain"],
)

langchainUtil = LangchainUtil()


class OpenaiCompletionMessage(BaseModel):
    role: Literal["system", "user"]
    content: str


class LangchainCompletionBody(BaseModel):
    message: str
    llm: LLModel


@langchainRouter.post("/complete/{model}")
async def openai(model: LLModel, body: LangchainCompletionBody):
    """Non-Streaming chat completion"""
    message = body.message
    return await langchainUtil.chat_completion(model, message)


# TODO under Construction
@langchainRouter.post("/test/")
async def llama():
    langchainUtil.test()
    pass
