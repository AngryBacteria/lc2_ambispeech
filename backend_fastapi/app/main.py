import asyncio
import time

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from starlette.middleware.cors import CORSMiddleware

from app.routers.llm_router import llmRouter
from app.routers.logging_router import loggingRouter
from app.routers.transcribe_router import transcribeRouter
from app.utils.azure_util import AzureUtil
from app.utils.logging_util import logger
from app.utils.mongo_util import MongoUtil
from app.utils.openai_util import OpenAIUtil

# start app and configure CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load dependencies
azure_util = AzureUtil()
mongo = MongoUtil()
openai_util = OpenAIUtil()

# load other routers
app.include_router(loggingRouter)
app.include_router(llmRouter)
app.include_router(transcribeRouter)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down the server. Closing the database connections....")
    mongo.client.close()


@app.get("/")
async def root():
    return "Hello World! The Ambient Speech Recognition Server is working"


# TODO: remove. Only for testing purpose to show that sync in async can block whole app
@app.get("/test")
async def test():
    print("start")
    print("sleeping 10 seconds async")
    await asyncio.sleep(5)
    print("sleeping 10 second sync")
    await run_in_threadpool(sync_function)
    return "cooooooooooool"


# TODO: remove. Only for testing purpose to show that sync in async can block whole app
def sync_function():
    time.sleep(10)
    return "asdada"
