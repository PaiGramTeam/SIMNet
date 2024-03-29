"""A module for parsing cookies."""

from http.cookies import SimpleCookie
from typing import Dict


def parse_cookie(cookie: str) -> Dict[str, str]:
    """
    Parses a cookie or header into a dictionary of key-value pairs.

    Args:
        cookie (str): The cookie or header to parse.

    Returns:
        Dict[str, str]: A dictionary of key-value pairs representing the parsed cookie.

    Example:
        >>> cookie = "sessionid=123456; expires=Fri, 31-Dec-2021 23:59:59 GMT; HttpOnly; Max-Age=31449600; Path=/"
        >>> parse_cookie(cookie)
        {'sessionid': '123456'}
    """
    cookie = SimpleCookie(cookie)

    return {str(k): v.value for k, v in cookie.items()}
