"""
Module for defining a ZenML pipeline for digital data extraction, transformation, and loading (ETL).

This module defines a ZenML pipeline `digital_data_etl` that processes a list of links by first retrieving or creating a user, and then crawling the provided links.
"""

from zenml import pipeline

from steps.etl import crawl_links, get_or_create_user


@pipeline
def digital_data_etl(user_full_name: str, links: list[str]) -> str:
    """
    ZenML pipeline for crawling digital data linked to a user.

    This pipeline retrieves or creates a user based on the provided full name, then crawls the given links.

    Args:
        user_full_name (str): The full name of the user.
        links (list[str]): A list of URLs to be crawled.

    Returns:
        str: The invocation ID of the last step in the pipeline execution.
    """
    user = get_or_create_user(user_full_name)
    last_step = crawl_links(user=user, links=links)

    return last_step.invocation_id