from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.llm import llmRouter
from app.routers.logging import loggingRouter
from app.utils.mongo_util import MongoUtil
from dotenv import load_dotenv

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
