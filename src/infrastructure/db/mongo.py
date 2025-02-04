from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from src.settings import settings

class MongoDatabaseConnector:
    """A singleton class to connect to MongoDB database.

    This class ensures that only one instance of the MongoClient is created
    and reused across the application. If the connection fails, an error message
    is logged, and the exception is raised.
    
    Attributes:
        _instance (MongoClient | None): A class-level attribute holding the
        MongoClient instance. It ensures that only one connection is made.
    """
    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs) -> MongoClient:
        """Create or return the existing MongoDB client instance.

        This method checks if an instance of MongoClient already exists.
        If not, it will create a new instance and connect to MongoDB using the
        credentials and host provided in the settings. If connection fails, it logs
        the error and raises an exception.

        Args:
            *args: Additional positional arguments passed to MongoClient (unused).
            **kwargs: Additional keyword arguments passed to MongoClient (unused).

        Returns:
            MongoClient: The singleton MongoClient instance.
        
        Raises:
            ConnectionFailure: If the connection to MongoDB fails.
        """
        if cls._instance is None:
            try:
                # Format the MongoDB host with the username and password from settings
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

