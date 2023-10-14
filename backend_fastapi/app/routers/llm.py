import datetime

from fastapi import APIRouter
from starlette.background import BackgroundTasks

from app.utils.llm_util import LLMUtil, OpenaiModel
from app.utils.mongo_util import LogEntry, Service, MongoUtil

llmRouter = APIRouter(
    prefix="/api/llm",
    tags=["llm"],
)


llmUtil = LLMUtil()


@llmRouter.post("/hello/{model}")
async def hello(model: OpenaiModel):
    llmUtil.openai_model = model
    return await llmUtil.create_hello_chat_completion()
