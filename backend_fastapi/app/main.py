import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.utils.MongoUtil import MongoDB
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dependencies
load_dotenv()
mongo = MongoDB(uri=os.getenv("MONGO_DB_URL"), db_name="main")


@app.get("/")
def root():
    return "Hello World! The Ambient Speech Recognition Server is working"


@app.get("/db/test")
async def test():
    document = await mongo.db.logs.find_one({'tokens': {'$gt': 1}}, {'_id': 0})
    print(document)
    return document
