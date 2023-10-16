import time

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from app.routers.llm_router import llmRouter
from app.routers.logging_router import loggingRouter
from app.utils.llm_util import LLMUtil
from app.utils.mongo_util import MongoUtil
from app.utils.speech_util import SpeechUtil

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
speech = SpeechUtil()
mongo = MongoUtil()
llm = LLMUtil()

# load other routers
app.include_router(loggingRouter)
app.include_router(llmRouter)


@app.on_event('shutdown')
def shutdown_event():
    print("Shutting down the server. Closing the database connections....")
    mongo.client.close()


@app.get("/")
async def root():
    return "Hello World! The Ambient Speech Recognition Server is working"


def fake_data_streamer():
    for i in range(10):
        yield f"some fake data [{i}]"
        time.sleep(1)


@app.get("/stream")
async def main():
    return StreamingResponse(fake_data_streamer(), media_type='text/event-stream')


@app.post("/file")
async def post_file(file: UploadFile):
    return {
        "size": file.size,
        "name": file.filename,
        "content_type": file.content_type
    }
