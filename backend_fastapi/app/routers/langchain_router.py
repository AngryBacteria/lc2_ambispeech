from typing import Literal

from fastapi import APIRouter

from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.utils.langchain_util import LangchainUtil

langchainRouter = APIRouter(
    prefix="/api/langchain",
    tags=["langchain"],
)

langchainUtil = LangchainUtil()



@langchainRouter.post("/hello/")
async def hello():
    """Hello World example for large language models"""
    return await langchainUtil.hello_chat_completion()

