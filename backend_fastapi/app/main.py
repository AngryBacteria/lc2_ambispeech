from fastapi import FastAPI, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware

from app.routers.langchain_router import langchainRouter
from app.routers.llm_router import llmRouter
from app.routers.transcribe_router import transcribeRouter
from app.utils.azure_util import AzureUtil
from app.utils.langchain_util import LangchainUtil
from app.utils.logging_util import logger
from app.utils.openai_util import OpenAIUtil
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


def write_notification():
    print("I am running after the response")

@app.get("/background")
async def background(background_tasks: BackgroundTasks):
    print("I am running before the response 1")
    background_tasks.add_task(write_notification)
    print("I am running before the response 2")
    return {"message": "Notification sent in the background"}
