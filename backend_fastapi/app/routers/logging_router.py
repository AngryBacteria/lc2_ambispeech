import datetime

from fastapi import APIRouter

from app.utils.mongo_util import Service, MongoUtil, LogEntry

loggingRouter = APIRouter(
    prefix="/api/db",
    tags=["db"],
)
mongo = MongoUtil()


@loggingRouter.get("/read")
async def test_log_read():
    items = await mongo.db['logs'].find({}, {'_id': 0}).to_list(length=20)
    return items


@loggingRouter.get("/write")
async def test_log_write():
    log = LogEntry(
        Service.TEST,
        datetime.datetime.now(),
        endpoint="/api/db/write"
    )
    await mongo.saveLog(log)
    return log
