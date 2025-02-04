from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from src.settings import settings

class MongoDatabaseConnector:
    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs) -> MongoClient:
        if cls._instance is None:
            try:
                mongodb_host = settings.MONGODB_DATABASE_HOST.format(
                    mongodb_username=settings.MONGODB_DATABASE_USERNAME,
                    mongodb_password=settings.MONGODB_DATABASE_PASSWORD
                    )
                cls._instance = MongoClient(mongodb_host)
            except ConnectionFailure as e:
                logger.error(f"couldn't connect to the database: {e!s}")

                raise
        
        logger.info(f"Connection to MongoDB with URI successfull: {settings.MONGODB_DATABASE_HOST}")

        return cls._instance
    
connection = MongoDatabaseConnector()

