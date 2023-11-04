from http.cookiejar import CookieJar
from http.cookies import SimpleCookie
from typing import Optional, TypeVar

from httpx import Cookies as _Cookies

from simnet.utils.types import CookieTypes

from pydantic import BaseModel

IntStr = TypeVar("IntStr", int, str)

__all__ = (
    "Cookies",
    "CookiesModel",
)


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
            if (
                cookie.name == name
                and domain is None
                or cookie.domain == domain
                and path is None
                or cookie.path == path
                and cookie.value
            ):
                value = cookie.value
        if value is None:
            return default
        return value


class CookiesModel(BaseModel, frozen=False):
    """A model that represents the cookies used by the client."""

    login_uid: Optional[IntStr] = None
    login_ticket: Optional[str] = None

    stoken: Optional[str] = None
    stuid: Optional[IntStr] = None
    mid: Optional[str] = None

    account_id: Optional[IntStr] = None
    cookie_token: Optional[str] = None

    ltoken: Optional[str] = None
    ltuid: Optional[IntStr] = None

    account_mid_v2: Optional[str] = None
    cookie_token_v2: Optional[str] = None
    account_id_v2: Optional[IntStr] = None

    ltoken_v2: Optional[str] = None
    ltmid_v2: Optional[str] = None
    ltuid_v2: Optional[IntStr] = None

    @property
    def is_v1(self) -> bool:
        if self.account_id or self.cookie_token or self.ltoken or self.ltuid:
            return True
        return False

    @property
    def is_v2(self) -> bool:
        if self.account_mid_v2 or self.cookie_token_v2 or self.ltoken_v2 or self.ltmid_v2:
            return True
        return False

    def remove_v2(self):
        """Remove the v2 cookies."""
        self.account_mid_v2 = None
        self.cookie_token_v2 = None
        self.ltoken_v2 = None
        self.ltmid_v2 = None

    def to_dict(self):
        """Return the cookies as a dictionary."""
        return self.dict(exclude_defaults=True)

    def to_json(self):
        """Return the cookies as a JSON string."""
        return self.json(exclude_defaults=True)

    @property
    def user_id(self) -> Optional[int]:
        if self.ltuid:
            return self.ltuid
        if self.account_id:
            return self.account_id
        if self.login_uid:
            return self.login_uid
        if self.stuid:
            return self.stuid
        if self.account_id_v2:
            return self.account_id_v2
        if self.ltuid_v2:
            return self.ltuid_v2
        return None

    def set_v2_uid(self, user_id: int):
        """Set the user ID for the v2 cookies."""
        if self.ltuid_v2 is None and self.ltoken_v2:
            self.ltuid_v2 = user_id
        if self.account_id_v2 is None and self.account_mid_v2:
            self.account_id_v2 = user_id

    def set_uid(self, user_id: int):
        """Set the user ID for the v1 cookies."""
        if self.account_id is None and self.cookie_token:
            self.account_id = user_id
        if self.ltuid is None and self.ltoken:
            self.ltuid = user_id
