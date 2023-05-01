from typing import Optional

from httpx import Cookies as _Cookies


class Cookies(_Cookies):
    """An extension of the `httpx.Cookies` class that includes additional functionality."""

    COOKIE_USER_ID_NAMES = ("ltuid", "account_id", "ltuid_v2", "account_id_v2")

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
