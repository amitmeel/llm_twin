import uuid
from abc import ABC
from typing import Generic, Type, TypeVar

from loguru import logger
from pydantic import UUID4, BaseModel, Field
from pymongo import errors

from src.domain.exceptions import ImproperlyConfigured
from src.infrastructure.db.mongo import connection
from src.settings import settings


# Initialize database connection
_database = connection.get_database(settings.MONGODB_DATABASE_NAME)

# Type variable for generic class implementation
T = TypeVar("T", bound="NoSQLBaseDocument")

class NoSQLBaseDocument(BaseModel, Generic[T], ABC):
    """
    Base document class for MongoDB models.

    This class provides basic MongoDB operations and UUID handling functionality.
    It uses Pydantic for data validation and serialization.

    Attributes:
        id: UUID4 field that serves as the primary identifier for the document.
            Automatically generated if not provided.
    """

    id: UUID4 = Field(default_factory=uuid.uuid4)
    

    def __eq__(self, value: object) -> bool:
        """Implements equality comparison based on document ID.

        Args:
            value: Object to compare with.

        Returns:
            bool: True if objects are of same type and have same ID, False otherwise.
        """
        if not isinstance(value, self.__class__):
            return False
        
        return self.id == value.id
    
    def __hash__(self) -> int:
        """Implements hashing based on document ID.

        Returns:
            int: Hash value of the document's ID.
        """
        return hash(self.id)
    
    @classmethod
    def from_mongo(cls: Type[T], data: dict) -> T:
        """Creates instance from MongoDB document format.

        Converts MongoDB's "_id" field to UUID "id" field expected by Pydantic model.

        Args:
            data: Dictionary containing MongoDB document data.

        Returns:
            T: Instance of the document class.

        Raises:
            ValueError: If input data is empty.
        """

        if not data:
            raise ValueError("Data is empty")
        
        id = data.pop("_id")

        return cls(**dict(data, id=id))
    
    def to_mongo(self: T, **kwargs) -> dict:
        """Converts instance to MongoDB document format.

        Handles conversion of UUID fields to strings and remaps 'id' to '_id'.

        Args:
            **kwargs: Additional arguments passed to model_dump().
                exclude_unset: Whether to exclude unset fields (default: False)
                by_alias: Whether to use field aliases (default: True)

        Returns:
            dict: Document data in MongoDB format.
        """
        # exclude_unset: Whether to exclude fields that have not been explicitly set.
        exclude_unset = kwargs.pop("exclude_unset", False)
        # by_alias: Whether to use the field's alias in the dictionary key if defined.
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(exclude_unset=exclude_unset, by_alias=by_alias, **kwargs)

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))

        # Convert all UUID fields to strings for MongoDB compatibility
        for key,value in parsed.items():
            if isinstance(value, uuid.UUID):
                parsed[key] = str(value)

        return parsed
    
    def model_dump(self: T, **kwargs) -> dict:
        """Override of Pydantic's model_dump to handle UUID serialization.

        Converts all UUID fields to strings in the output dictionary.

        Args:
            **kwargs: Arguments passed to parent's model_dump.

        Returns:
            dict: Model data with UUID fields converted to strings.
        """
        dict_ = super().model_dump(**kwargs)

        # Convert all UUID fields to strings
        for key, value in dict_.items():
            if isinstance(value, uuid.UUID):
                dict_[key] = str(value)

        return dict_
    
    def save(self: T, **kwargs) -> T | None:
        """Saves document to MongoDB collection.

        Args:
            **kwargs: Additional arguments passed to to_mongo().

        Returns:
            T | None: Self if save successful, None if failed.
        """
        collection = _database[self.get_collection_name()]

        try:
            collection.insert_one(self.to_mongo(**kwargs))

            return self
        except errors.WriteError:
            logger.error("Failed to insert document.")

            return None
        
    @classmethod
    def get_or_create(cls: Type[T], **filter_options) -> T:
        """Retrieves document matching filter or creates new one if not found.

        Args:
            **filter_options: Filter criteria for document lookup.

        Returns:
            T: Retrieved or newly created document.

        Raises:
            errors.OperationFailure: If MongoDB operation fails.
        """
        collections = _database[cls.get_collection_name()]
        try:
            # Try to find existing document
            instance = collections.find_one(filter_options)
            if instance:
                return cls.from_mongo(instance)
            
            # Create new document if not found
            new_instance = cls(**filter_options)
            new_instance = new_instance.save()

            return new_instance
        except errors.OperationFailure:
            logger.exception(f"Failed to retrieve document with filter options: {filter_options}")

            raise

    @classmethod
    def bulk_insert(cls: Type[T], documents: list[T], **kwargs) -> bool:
        """Inserts multiple documents in a single operation.

        Args:
            documents: List of document instances to insert.
            **kwargs: Additional arguments passed to to_mongo().

        Returns:
            bool: True if successful, False if operation failed.
        """
        collection = _database[cls.get_collection_name()]
        try:
            collection.insert_many(doc.to_mongo(**kwargs) for doc in documents)

            return True
        except (errors.WriteError, errors.BulkWriteError):
            logger.error(f"Failed to insert documents of type {cls.__name__}")

            return False
    

    def get_collection_name(cls: Type[T]) -> str:
        """Gets MongoDB collection name from Settings class.

        This method expects child classes to define a nested 'Settings' class with a 'name' attribute.
        The 'Settings' class serves as a configuration class for document-specific settings.

        ```python
        Example:
            class UserDocument(NoSQLBaseDocument):
                class Settings:
                    name = "users"  # Specifies the MongoDB collection name
                
            first_name: str
            last_name: str
        ```

        Returns:
            str: Name of the MongoDB collection specified in Settings.name.

        Raises:
            ImproperlyConfigured: If child class doesn't define Settings class
                or Settings class doesn't have 'name' attribute.
        """
        if not hasattr(cls, "Settings") or not hasattr(cls.Settings, "name"):
            raise ImproperlyConfigured(
                "Document should define an Settings configuration class with the name of the collection."
            )
        
        return cls.Settings.name

