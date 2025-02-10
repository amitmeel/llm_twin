from src.domain.exceptions import ImproperlyConfigured

def split_user_full_name(user: str|None) -> tuple[str, str]:
    """
    Splits a full name into first and last names.

    Args:
        user (str | None): The full name as a string.

    Returns:
        tuple[str, str]: A tuple containing the first name and last name.

    Raises:
        ImproperlyConfigured: If the input is None or an empty string.
    """
    if not user or not user.strip():
        raise ImproperlyConfigured("User name is empty")

    name_tokens = user.split(" ")
    if len(name_tokens) == 0:
        raise ImproperlyConfigured("User name is empty")
    elif len(name_tokens) == 1:
        first_name, last_name = name_tokens[0], name_tokens[0]
    else:
        first_name, last_name = " ".join(name_tokens[:-1]), name_tokens[-1]

    return first_name, last_name