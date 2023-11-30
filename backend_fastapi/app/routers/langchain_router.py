from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel

from app.utils.langchain_util import LangchainUtil, LLModel

langchainRouter = APIRouter(
    prefix="/api/langchain",
    tags=["langchain"],
)

langchainUtil = LangchainUtil()


# TODO not used, should be deleted, if not reimplemented
class OpenaiCompletionMessage(BaseModel):
    role: Literal["system", "user"]
    content: str


class LangchainCompletionBody(BaseModel):
    message: str
    llm: LLModel


@langchainRouter.post("/complete/{model}")
async def langchain(model: LLModel, body: LangchainCompletionBody):
    """Non-Streaming chat completion"""
    transcript = body.message
    return await langchainUtil.chat_completion(model, transcript)


@langchainRouter.post("/test/")
async def test():
    """Non-Streaming chat completion"""
    return await langchainUtil.test()
