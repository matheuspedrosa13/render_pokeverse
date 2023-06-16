import pymongo
from src.utils.env_config.util import config


class MongoDBInfra:
    __client = None
    __user = config("MONGO_USER")
    __password = config("MONGO_PASSWORD")
    __url = config("MONGO_URL")

    @classmethod
    def get_client(cls):
        if cls.__client is None:
            cls.__client = pymongo.MongoClient(f"mongodb+srv://{cls.__user}:{cls.__password}@{cls.__url}")
        return cls.__client
