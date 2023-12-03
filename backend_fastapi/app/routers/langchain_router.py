from fastapi import APIRouter
from pydantic import BaseModel

from app.utils.langchain_util import LangchainUtil, LLModel

langchainRouter = APIRouter(
    prefix="/api/langchain",
    tags=["langchain"],
)

langchainUtil = LangchainUtil()


class LangchainCompletionBody(BaseModel):
    message: str


@langchainRouter.post("/hello/{model}")
async def hello(model: LLModel):
    """Hello World example for large language models with langchain"""
    return await langchainUtil.hello_chat_completion(model)


@langchainRouter.post("/complete/{model}")
async def langchain(model: LLModel, body: LangchainCompletionBody):
    """Non-Streaming chat completion"""
    transcript = body.message
    return await langchainUtil.chat_completion(model, transcript)


@langchainRouter.post("/test/{model}")
async def test(model: LLModel, body: LangchainCompletionBody):
    """Non-Streaming chat completion"""
    return await langchainUtil.test(model, body.message)
