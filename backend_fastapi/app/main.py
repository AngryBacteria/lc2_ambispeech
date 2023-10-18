import time

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from app.routers.llm_router import llmRouter
from app.routers.logging_router import loggingRouter
from app.routers.transcribe_router import transcribeRouter
from app.utils.openai_util import OpenAIUtil
from app.utils.mongo_util import MongoUtil
from app.utils.azure_util import AzureUtil

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
    print("Shutting down the server. Closing the database connections....")
    mongo.client.close()


@app.get("/")
async def root():
    return "Hello World! The Ambient Speech Recognition Server is working"
