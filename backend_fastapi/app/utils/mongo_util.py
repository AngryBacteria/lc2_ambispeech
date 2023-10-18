from __future__ import annotations

import datetime
import os
from enum import Enum

import motor.motor_asyncio
from dotenv import load_dotenv

from app.utils.logging_util import logger


class MongoUtil:
    _instance = None
    _client: motor.motor_asyncio.AsyncIOMotorClient = None
    _db: motor.motor_asyncio.AsyncIOMotorDatabase = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        if os.getenv("MONGO_DB_URL") is None:
            raise EnvironmentError(".env file is missing the MONGO_DB_URL")

        if MongoUtil._client is None:
            MongoUtil._client = motor.motor_asyncio.AsyncIOMotorClient(
                os.getenv("MONGO_DB_URL")
            )
        if MongoUtil._db is None:
            MongoUtil._db = MongoUtil._client["main"]

    @property
    def client(self):
        return MongoUtil._client

    @property
    def db(self):
        return MongoUtil._db

    async def saveLog(self, log: LogEntry):
        try:
            await self.db.logs.insert_one(log.get_json())
        except IOError as error:
            logger.error(f"Error while saving log: {error}")


# database objects
class Service(Enum):
    OPENAI = "openai"
    DEEPINFRA = "deepinfra"
    AZURE = "azure"
    TEST = "test_service"


class LLMModel(Enum):
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"


class LogEntry:
    service: Service
    date: datetime
    endpoint: str

    def __init__(self, service: Service, date: datetime, endpoint: str):
        self.service = service
        self.date = date
        self.endpoint = endpoint

    def get_json(self):
        return {
            "date": self.date,
            "service": self.service.name,
            "endpoint": self.endpoint,
        }


class LLMLogEntry(LogEntry):
    model: LLMModel
    tokens: int

    def __init__(
        self,
        service: Service,
        date: datetime,
        endpoint: str,
        model: LLMModel,
        tokens: int,
    ):
        super().__init__(service, date, endpoint)
        self.model = model
        self.tokens = tokens

    def get_json(self):
        return {
            "date": self.date,
            "service": self.service.value,
            "endpoint": self.endpoint,
            "length": self.model.value,
            "tokens": self.tokens,
        }


class S2TLogEntry(LogEntry):
    length: int

    def __init__(self, service: Service, date: datetime, endpoint: str, length: int):
        super().__init__(service, date, endpoint)
        self.length = length

    def get_json(self):
        return {
            "date": self.date,
            "service": self.service.value,
            "endpoint": self.endpoint,
            "length": self.length,
        }
