import asyncio
import time

from fastapi import FastAPI, UploadFile
from fastapi.concurrency import run_in_threadpool
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.routers.llm_router import llmRouter
from app.routers.logging_router import loggingRouter
from app.routers.transcribe_router import transcribeRouter
from app.routers.langchain_router import langchainRouter
from app.utils.azure_util import AzureUtil
from app.utils.logging_util import logger
from app.utils.mongo_util import MongoUtil
from app.utils.openai_util import OpenAIUtil
from app.utils.langchain_util import LangchainUtil
from app.utils.whisper_util import WhisperUtil

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
openai_util = OpenAIUtil()
langchain_util = LangchainUtil
whisper_util = WhisperUtil()

# load other routers
app.include_router(llmRouter)
app.include_router(transcribeRouter)
app.include_router(langchainRouter)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down the server")


@app.get("/")
async def root():
    return "Hello World! The Ambient Speech Recognition Server is working"


def fakeStream():
    for i in range(4):
        yield f"Data {i}"
        time.sleep(1)


@app.post("/fakefilestream")
async def create_upload_file(file: UploadFile):
    print({"filename": file.filename, "bytes": file.size})
    return StreamingResponse(
        fakeStream(),
        media_type="text/event-stream",
    )
