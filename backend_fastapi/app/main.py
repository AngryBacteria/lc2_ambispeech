import asyncio
import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.llm_router import llmRouter
from app.routers.logging_router import loggingRouter
from app.utils.mongo_util import MongoUtil
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

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
load_dotenv()
mongo = MongoUtil()

# load other routes
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
