"""Base Selenium Crawler Module.

This module defines abstract base classes for web crawlers, specifically using Selenium for web scraping.

Classes:
    BaseCrawler: Abstract base class for web crawlers.
    BaseSeleniumCrawler: Abstract base class for Selenium-based web crawlers.

"""

import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.domain.documents import NoSQLBaseDocument

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()


class BaseCrawler(ABC):
    """Abstract base class for web crawlers.

    Attributes:
        model (type[NoSQLBaseDocument]): Model representing the document structure.
    """
    model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None:
        """Extracts data from the given link.

        Args:
            link (str): The URL to extract data from.
            **kwargs: Additional arguments for extraction.
        """
        ...


class BaseSeleniumCrawler(BaseCrawler, ABC):
    """Abstract base class for Selenium-based web crawlers.

    Attributes:
        scroll_limit (int): Maximum number of times to scroll down the page.
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """
    def __init__(self, scroll_limit: int = 5) -> None:
        """Initializes the Selenium WebDriver with necessary options.

        Args:
            scroll_limit (int, optional): Maximum number of scrolls. Defaults to 5.
        """
        options = webdriver.ChromeOptions

        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9226")

        self.set_extra_driver_options(options)
        self.scroll_limit = scroll_limit
        self.driver = webdriver.Chrome(
            options=options,
        )

    def set_extra_driver_options(self, options: Options) -> None:
        """Allows subclasses to set additional driver options.

        Args:
            options (Options): Selenium ChromeOptions instance.
        """
        pass

    def login(self) -> None:
        """Handles login functionality for the crawler.
        This method should be implemented by subclasses.
        """
        pass

    def scroll_page(self) -> None:
        """Scrolls through the page based on the scroll limit.

        This function scrolls to the bottom of the page iteratively until 
        either the scroll limit is reached or no further scrolling is possible.
        """
        current_scroll = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height==last_height or (self.scroll_limit and current_scroll>self.scroll_limit):
                break
            last_height = new_height
            current_scroll += 1