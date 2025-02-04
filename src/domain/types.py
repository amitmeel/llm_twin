from enum import StrEnum


class DataCategory(StrEnum):
    """Enum class representing various data categories.

    This class defines different categories for organizing data within the system.
    Each category is represented as a string value for easy use in database queries, 
    file handling, or data processing tasks.

    Attributes:
        PROMPT (str): The category for prompt data.
        QUERIES (str): The category for query data.
        INSTRUCT_DATASET_SAMPLES (str): The category for instruction dataset samples.
        INSTRUCT_DATASET (str): The category for instruction dataset data.
        PREFERENCE_DATASET_SAMPLES (str): The category for preference dataset samples.
        PREFERENCE_DATASET (str): The category for preference dataset data.
        POSTS (str): The category for posts.
        ARTICLES (str): The category for articles.
        REPOSITORIES (str): The category for repositories.
    """

    PROMPT = "prompt"
    QUERIES = "queries"

    INSTRUCT_DATASET_SAMPLES = "instruct_dataset_samples"
    INSTRUCT_DATASET = "instruct_dataset"
    PREFERENCE_DATASET_SAMPLES = "preference_dataset_samples"
    PREFERENCE_DATASET = "preference_dataset"

    POSTS = "posts"
    ARTICLES = "articles"
    REPOSITORIES = "repositories"
