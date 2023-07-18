from http.cookiejar import CookieJar
from http.cookies import SimpleCookie
from typing import Optional

from httpx import Cookies as _Cookies

from simnet.utils.types import CookieTypes

__all__ = ("Cookies",)


class Cookies(_Cookies):
    """A wrapper around `httpx.Cookies` that provides additional functionality."""

    jar: CookieJar

    def __init__(self, cookies: Optional[CookieTypes] = None):  # skipcq: PYL-W0231
        self.jar = CookieJar()
        if cookies is None or isinstance(cookies, dict):
            if isinstance(cookies, dict):
                for key, value in cookies.items():
                    if isinstance(value, str):
                        self.set(key, value)
                    else:
                        self.set(key, str(value))
        elif isinstance(cookies, list):
            for key, value in cookies:
                self.set(key, value)
        elif isinstance(cookies, Cookies):
            for cookie in cookies.jar:
                self.jar.set_cookie(cookie)
        elif isinstance(cookies, str):
            cookie = SimpleCookie(cookies)
            for key, value in cookie.items():
                self.set(key, value.value)
        else:
            self.jar = cookies  # type: ignore

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

    def get(
        self,
        name: str,
        default: Optional[str] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
    ) -> Optional[str]:
        """
        Get a cookie by name. May optionally include domain and path
        in order to specify exactly which cookie to retrieve.
        """
        value = None
        for cookie in self.jar:
            if cookie.name == name:
                if domain is None or cookie.domain == domain:
                    if path is None or cookie.path == path:
                        if cookie.value:
                            value = cookie.value
        if value is None:
            return default
        return value
