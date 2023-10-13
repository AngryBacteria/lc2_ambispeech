import datetime
import os

import motor.motor_asyncio
from enum import Enum

from dotenv import load_dotenv


class MongoDB:
    _instance = None
    _client: motor.motor_asyncio.AsyncIOMotorClient = None
    _db: motor.motor_asyncio.AsyncIOMotorDatabase = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        if os.getenv("MONGO_DB_URL") is None:
            raise Exception(".env file is missing the MONGO_DB_URL")

        if MongoDB._client is None:
            MongoDB._client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_DB_URL"))
        if MongoDB._db is None:
            MongoDB._db = MongoDB._client["main"]

    @property
    def client(self):
        return MongoDB._client

    @property
    def db(self):
        return MongoDB._db


# database objects
class Service(Enum):
    OPENAI = "openai"
    DEEPINFRA = "deepinfra"
    AZURE = "azure"


class Model(Enum):
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_3_TURBO_16k = "gpt-3.5-turbo-16k"


class LogEntry:
    service: Service
    date: datetime

    def __init__(self, service: Service, date: datetime):
        self.service = service
        self.date = date

    def get_json(self):
        return {
            "date": self.date,
            "service": self.service.name,
        }


class LLMLogEntry(LogEntry):
    model: Model
    tokens: int

    def __init__(self, service: Service, date: datetime, model: Model, tokens: int):
        super().__init__(service, date)
        self.model = model
        self.tokens = tokens

    def get_json(self):
        return {
            "date": self.date,
            "service": self.service.name,
            "length": self.model.name,
            "tokens": self.tokens
        }


class S2TLogEntry(LogEntry):
    length: int

    def __init__(self, service: Service, date: datetime, length: int):
        super().__init__(service, date)
        self.length = length

    def get_json(self):
        return {
            "date": self.date,
            "service": self.service.name,
            "length": self.length
        }
