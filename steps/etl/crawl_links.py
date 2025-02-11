"""
Module for crawling links using a dispatcher-based approach.

This module defines a ZenML step `crawl_links` that processes a list of links using registered crawlers. It also provides helper functions for crawling individual links and updating metadata.
"""
from urllib.parse import urlparse

from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from src.application.crawlers.dispatcher import CrawlerDispatcher
from src.domain.documents import  UserDocument


@step
def crawl_links(user: UserDocument, links: list[str]) -> Annotated[list[str], "crawled_links"]:
    """
    Crawls the provided links using registered crawlers and records metadata.

    Args:
        user (UserDocument): The user document containing user-specific data.
        links (list[str]): A list of URLs to be crawled.

    Returns:
        list[str]: The input list of links after crawling.
    """
    # Initialize the dispatcher and register supported crawlers
    dispatcher = CrawlerDispatcher.build().register_linkedin().register_medium().register_github()

    logger.info(f"Start to crawl {len(links)} links(s)")

    metadata = {}  # Dictionary to store metadata about crawled domains
    successfull_crawls = 0  # Counter for successfully crawled links
    for link in tqdm(links):
        successfull_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
        successfull_crawls += successfull_crawl
        
        metadata = _add_to_metadata(metadata, crawled_domain, successfull_crawl)

    # Store metadata in the ZenML step context
    step_context = get_step_context()
    step_context.add_output_metadata(output_name='crawled_links', metadata=metadata)

    logger.info(f"Successfully crawled {successfull_crawls} / {len(links)} links.")

    return links

def _crawl_link(dispatcher: CrawlerDispatcher, link: str, user: UserDocument) -> tuple[bool, str]:
    """
    Crawls a single link using the appropriate crawler from the dispatcher.

    Args:
        dispatcher (CrawlerDispatcher): The dispatcher managing different crawlers.
        link (str): The URL to be crawled.
        user (UserDocument): The user document containing user-specific data.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating success, and the domain of the crawled link.
    """
    # Get the appropriate crawler for the link
    crawler = dispatcher.get_crawler(link)
    # Extract domain name from the URL
    craler_domain = urlparse(link).netloc

    try:
        # Extract content from the link
        crawler.extract(link=link, user=user)

        return (True, craler_domain)
    except Exception as e:
        logger.error(f"An error occured while crawling: {e!s}")

        return (False, craler_domain)
    
def _add_to_metadata(metadata: dict, domain: str, successfull_crawl: bool) -> dict:
    """
    Updates the metadata dictionary with the crawling result of a given domain.

    Args:
        metadata (dict): The metadata dictionary storing crawl results.
        domain (str): The domain name of the crawled link.
        successful_crawl (bool): Whether the crawl was successful or not.

    Returns:
        dict: Updated metadata dictionary.
    """
    if domain not in metadata:
        metadata[domain] = {}

    metadata[domain]["successfull"] = metadata.get(domain, {}).get("successfull", 0) + successfull_crawl
    metadata[domain]["total"] = metadata.get(domain, {}).get("total", 0) + 1

    return metadata