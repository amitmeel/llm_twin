from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step

from src.application import utils
from src.domain.documents import UserDocument


@step
def get_or_create_user(user_full_name: str) -> Annotated[UserDocument, "user"]:
    """
    Retrieves an existing user or creates a new one if not found.

    Args:
        user_full_name (str): The full name of the user.

    Returns:
        UserDocument: The retrieved or newly created user document.
    """
    logger.info(f"Getting or creating user: {user_full_name}")

    # Splitting user name into first and last names
    first_name, last_name = utils.split_user_full_name(user_full_name)

    # Retrieve or create user in the database
    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    # Fetch step context and log metadata
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="user", metadata=_get_metadata(user_full_name, user))

    return user


def _get_metadata(user_full_name: str, user: UserDocument) -> dict[str, dict]:
    """
    Generates metadata for logging and debugging purposes.

    Args:
        user_full_name (str): The original full name input.
        user (UserDocument): The retrieved or created user.

    Returns:
        dict[str, dict]: Structured metadata information.
    """
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "user_id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }
