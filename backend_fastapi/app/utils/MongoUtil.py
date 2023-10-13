import motor.motor_asyncio


class MongoDB:
    _instance = None
    _client = None
    _db = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri, db_name):
        if MongoDB._client is None:
            MongoDB._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        if MongoDB._db is None:
            MongoDB._db = MongoDB._client[db_name]

    @property
    def client(self):
        return MongoDB._client

    @property
    def db(self):
        return MongoDB._db
