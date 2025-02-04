from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory


class UserDocument(NoSQLBaseDocument):
    """Represents a user document in the NoSQL database.
    
    This class extends the `NoSQLBaseDocument` and defines attributes specific to
    a user, such as `first_name` and `last_name`. It also includes a `full_name`
    property to combine these two fields into a complete name.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """
    first_name: str
    last_name: str

    class Settings:
        """Settings for the UserDocument.
        
        This class defines the name of the collection in the database as 'users'.
        """
        name = "users"

    @property
    def full_name(self):
        """Returns the full name by combining `first_name` and `last_name`.
        
        Returns:
            str: The full name of the user in the format 'First Last'.
        """
        return f"{self.first_name} {self.last_name}"
    
class Document(NoSQLBaseDocument, ABC):
    """Represents a generic document in the NoSQL database.

    This is a base class for documents containing common attributes such as
    `content`, `platform`, and information about the author (via `author_id` and 
    `author_full_name`). It extends both `NoSQLBaseDocument` and `ABC` (abstract 
    base class).

    Attributes:
        content (dict): The content of the document.
        platform (str): The platform from which the document was published.
        author_id (UUID4): The ID of the author (UUID).
        author_full_name (str): The full name of the author.
    """
    content: dict
    platform: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")

class Repositorylink(Document):
    """Represents a repository link document in the NoSQL database.

    This class extends the `Document` class and adds specific fields for repositories.
    It also defines the collection name for repository links as a `DataCategory.REPOSITORIES`.

    Attributes:
        name (str): The name of the repository.
        link (str): The URL link to the repository.
    """
    name: str
    link: str

    class Settings:
        """Settings for the Repositorylink document.
        
        The name of the collection in the database is set to `DataCategory.REPOSITORIES`.
        """
        name = DataCategory.REPOSITORIES

class PostDocument(Document):
    """Represents a post document in the NoSQL database.

    This class extends the `Document` class and adds fields specific to posts. 
    The `image` and `link` fields are optional and represent an image URL and 
    an optional link to the post content.

    Attributes:
        image (Optional[str]): The URL to the image associated with the post.
        link (str | None): The URL link to the post (can be None).
    """
    image: Optional[str] = None
    link: str | None = None

    class Settings:
        """Settings for the PostDocument.
        
        The name of the collection in the database is set to `DataCategory.POSTS`.
        """
        name = DataCategory.POSTS


class ArticleDocument(Document):
    """Represents an article document in the NoSQL database.

    This class extends the `Document` class and adds a `link` field specific to articles.
    The `link` is a required attribute, representing the URL to the article.

    Attributes:
        link (str): The URL to the article.
    """
    link: str

    class Settings:
        """Settings for the ArticleDocument.
        
        The name of the collection in the database is set to `DataCategory.ARTICLES`.
        """
        name = DataCategory.ARTICLES
