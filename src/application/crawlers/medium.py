from bs4 import BeautifulSoup
from loguru import logger

from src.domain.documents import ArticleDocument

from .base import BaseSeleniumCrawler


class MediumCrawler(BaseSeleniumCrawler):
    """Crawler for extracting article content from Medium using Selenium.
    
    This crawler fetches Medium articles, extracts the title, subtitle, and full content,
    and saves the extracted data to the database.
    
    Attributes:
        model (ArticleDocument): The database model used for storing article data.
    """
    model = ArticleDocument

    def set_extra_driver_options(self, options) -> None:
        """Sets additional options for the Selenium WebDriver.
        
        Args:
            options: The Selenium WebDriver options instance.
        """
        options.add_argument(r"--profile-directory=Profile 2")

    def extract(self, link: str, **kwargs) -> None:
        """Extracts and saves a Medium article from the given link.
        
        If the article already exists in the database, it logs a message and returns early.
        Otherwise, it scrapes the page using Selenium, extracts the title, subtitle,
        and content, and stores the data in the database.
        
        Args:
            link (str): The URL of the Medium article to scrape.
            **kwargs: Additional arguments, including:
                - user: The user instance, containing `id` and `full_name`, who is saving the article.
        """
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")

            return

        logger.info(f"Starting scrapping Medium article: {link}")

        self.driver.get(link)
        self.scroll_page()

        # Parse page content using BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        title = soup.find_all("h1", class_="pw-post-title")  # Extract article title
        subtitle = soup.find_all("h2", class_="pw-subtitle-paragraph")  # Extract subtitle

        data = {
            "Title": title[0].string if title else None,
            "Subtitle": subtitle[0].string if subtitle else None,
            "Content": soup.get_text(),
        }

        self.driver.close()

        user = kwargs["user"]
        instance = self.model(
            platform="medium",
            content=data,
            link=link,
            author_id=user.id,
            author_full_name=user.full_name,
        )
        # Save extracted data to the database
        instance.save()

        logger.info(f"Successfully scraped and saved article: {link}")
