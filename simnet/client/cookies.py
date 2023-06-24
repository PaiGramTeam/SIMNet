from http.cookiejar import CookieJar
from http.cookies import SimpleCookie
from typing import Optional

from httpx import Cookies as _Cookies

from simnet.utils.types import CookieTypes

__all__ = ("Cookies",)


class Cookies(_Cookies):
    """A wrapper around `httpx.Cookies` that provides additional functionality.

    Args:
        cookies (Optional[CookieTypes], optional): The cookies to initialize the wrapper with.
            Can be a `dict`, a `list` of tuples, a `str`, or a `httpx.Cookies` object.
            Defaults to `None`.
    """

    def __init__(self, cookies: Optional[CookieTypes] = None):
        if cookies is None or isinstance(cookies, dict):
            self.jar = CookieJar()
            if isinstance(cookies, dict):
                for key, value in cookies.items():
                    if isinstance(value, str):
                        self.set(key, value)
                    else:
                        self.set(key, str(value))
        elif isinstance(cookies, list):
            self.jar = CookieJar()
            for key, value in cookies:
                self.set(key, value)
        elif isinstance(cookies, Cookies):
            self.jar = CookieJar()
            for cookie in cookies.jar:
                self.jar.set_cookie(cookie)
        elif isinstance(cookies, str):
            cookie = SimpleCookie(cookies)
            for key, value in cookie.items():
                self.set(key, value.value)
        else:
            self.jar = cookies

    COOKIE_USER_ID_NAMES = ("ltuid", "account_id", "stuid", "ltuid_v2", "account_id_v2")

    @property
    def account_id(self) -> Optional[int]:
        """Return the user account ID if present in the cookies.

        If one of the user ID cookies exists in the cookies, return its integer value.
        Otherwise, return `None`.

        Returns:
            Optional[int]: The user account ID, or `None` if it is not present in the cookies.
        """
        for name in self.COOKIE_USER_ID_NAMES:
            value = self.get(name)
            if value is not None:
                return int(value)
        return None
