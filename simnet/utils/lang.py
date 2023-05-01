def create_short_lang_code(lang: str) -> str:
    """
    Create a short language code from a longer one.

    This function takes a language code as input and returns a shortened version of it. If the language code contains
    "zh", the function returns the original code. Otherwise, the function returns the first part of the code (before the
    first hyphen, if there is one).

    Args:
        lang (str): The language code to be shortened.

    Returns:
        str: The shortened language code.
    """
    return lang if "zh" in lang else lang.split("-")[0]
