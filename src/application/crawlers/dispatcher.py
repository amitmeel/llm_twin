import re
from urllib.parse import urlparse

from loguru import logger

from .base import BaseCrawler
from .custom_article import CustomArticleCrawler
from .github import GithubCrawler
from .linkedin import LinkedInCrawler
from .medium import MediumCrawler

class CrawlerDispatcher:
    """
    A dispatcher class that manages and retrieves crawlers based on the given URL.
    
    This class maintains a registry of different crawlers for specific domains and 
    provides methods to retrieve the appropriate crawler based on a given URL.
    """
    
    def __init__(self) -> None:
        """Initializes an empty crawler registry."""
        self._crawlers = {}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        """
        Creates and returns an instance of CrawlerDispatcher.
        
        Returns:
            CrawlerDispatcher: A new instance of CrawlerDispatcher.
        """
        return cls()

    def register_medium(self) -> "CrawlerDispatcher":
        """
        Registers the Medium crawler.
        
        Returns:
            CrawlerDispatcher: The current instance with MediumCrawler registered.
        """
        self.register("https://medium.com", MediumCrawler)
        return self

    def register_linkedin(self) -> "CrawlerDispatcher":
        """
        Registers the LinkedIn crawler.
        
        Returns:
            CrawlerDispatcher: The current instance with LinkedInCrawler registered.
        """
        self.register("https://linkedin.com", LinkedInCrawler)
        return self

    def register_github(self) -> "CrawlerDispatcher":
        """
        Registers the GitHub crawler.
        
        Returns:
            CrawlerDispatcher: The current instance with GithubCrawler registered.
        """
        self.register("https://github.com", GithubCrawler)
        return self

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        """
        Registers a crawler for a given domain.
        
        Args:
            domain (str): The base URL of the website to register the crawler for.
            crawler (type[BaseCrawler]): The crawler class to handle the domain.
        """
        parsed_domain = urlparse(domain)
        domain = parsed_domain.netloc  # Extracts the domain name from the URL

        # Stores the crawler with a regex pattern to match URLs of the given domain
        self._crawlers[r"https://(www\.)?{}/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        """
        Retrieves the appropriate crawler based on the given URL.
        
        Args:
            url (str): The URL to find a corresponding crawler for.
        
        Returns:
            BaseCrawler: An instance of the matched crawler, or CustomArticleCrawler if no match is found.
        """
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):  # Checks if the URL matches any registered pattern
                return crawler()
        
        # Logs a warning and defaults to CustomArticleCrawler if no matching crawler is found
        logger.warning(f"No crawler found for {url}. Defaulting to CustomArticleCrawler.")
        return CustomArticleCrawler()
