from fastapi import APIRouter
from pydantic import BaseModel

from app.data.data import LLMService
from app.utils.langchain_util import LangchainUtil

langchainRouter = APIRouter(
    prefix="/api/langchain",
    tags=["langchain"],
)

langchainUtil = LangchainUtil()


class LangchainCompletionBody(BaseModel):
    message: str


@langchainRouter.post("/hello/{model}")
def hello(model: LLMService):
    """Hello World example for large language models with langchain"""
    return langchainUtil.hello_chat_completion(model)


@langchainRouter.post("/complete/{model}")
def langchain(model: LLMService, body: LangchainCompletionBody):
    """Non-Streaming chat completion"""
    transcript = body.message
    return langchainUtil.chat_completion(model, transcript)


@langchainRouter.post("/test/{model}")
def test(model: LLMService, body: LangchainCompletionBody):
    """Non-Streaming chat completion"""
    return langchainUtil.test(model, body.message)
