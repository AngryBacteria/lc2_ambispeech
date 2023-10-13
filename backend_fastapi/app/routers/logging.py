import datetime
import os

from dotenv import load_dotenv
from fastapi import APIRouter

from app.utils.mongo import LLMLogEntry, Service, Model, MongoDB

loggingRouter = APIRouter(
    prefix="/db",
    tags=["db"],
)
mongo = MongoDB()


@loggingRouter.get("/read")
async def test_log_read():
    items = await mongo.db['logs'].find({}, {'_id': 0}).to_list(length=20)
    return items


@loggingRouter.get("/write")
async def test_log_write():
    log = LLMLogEntry(
        Service.DEEPINFRA,
        datetime.datetime.now(),
        tokens=23487,
        model=Model.GPT_4
    )
    await mongo.db['logs'].insert_one(log.get_json())
    return log
