from urllib.parse import urlparse

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers.html2text import Html2TextTransformer
from loguru import logger

from src.domain.documents import ArticleDocument

from.base import BaseCrawler


class CustomArticleCrawler(BaseCrawler):
    """Custom crawler for extracting and saving article content from a given URL.

    Attributes:
        model (ArticleDocument): The document model used for storing articles.
    """
    model = ArticleDocument

    def __init__(self) -> None:
        """Initializes the CustomArticleCrawler instance."""
        super().__init__()

    def extract(self, link:str, **kwargs) -> None:
        """Extracts an article from the provided URL and stores it in the database.
 
        Args:
            link (str): The URL of the article to be scraped.
            **kwargs: Additional arguments, including:
                user (User): The user performing the extraction, providing `id` and `full_name` attributes.

        Returns:
            None

        Raises:
            KeyError: If the `user` key is missing in kwargs.
        """
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article exists in database: {link}")

            return
        
        logger.info(f"Starting scrapping article: {link}")

        loader = AsyncHtmlLoader([link])
        docs = loader.load()

        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)
        doc_transformed = docs_transformed[0]

        content = {
            "Title": doc_transformed.metadata.get("title"),
            "Subtitle": doc_transformed.metadata.get("description"),
            "Content": doc_transformed.page_content,
            "language": doc_transformed.metadata.get("language"),
        }

        parsed_url = urlparse(link)
        platform = parsed_url.netloc

        user = kwargs["user"]
        instance = self.model(
            content=content,
            link=link,
            platform=platform,
            author_id=user.id,
            author_full_name=user.full_name,
        )
        instance.save()

        logger.info(f"Finished scrapping custom article: {link}")