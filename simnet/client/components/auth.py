from typing import Optional, NoReturn

from simnet.client.base import BaseClient
from simnet.client.routes import (
    AUTH_URL,
    AUTH_KEY_URL,
    HK4E_LOGIN_URL,
    PASSPORT_URL,
)
from simnet.errors import RegionNotSupported
from simnet.utils.enum_ import Region

__all__ = ("AuthClient",)


class AuthClient(BaseClient):
    """
    The AuthClient class is a client for authentication services.
    It is derived from the BaseClient class and provides methods for retrieving
    different authentication tokens and keys.
    """

    async def get_stoken_by_login_ticket(
        self, login_ticket: Optional[str] = None, account_id: Optional[int] = None
    ) -> Optional[str]:
        """
        Retrieves a super ticket (`stoken`) using a login ticket (`login_ticket`) .

        Args:
            login_ticket (Optional[str]): The login ticket to use to retrieve the super ticket. If not provided, the
                `login_ticket` cookie value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the super ticket. If not provided, the
                `account_id` attribute value will be used.

        Returns:
            Optional[str]: The retrieved super ticket (`stoken`).

        Raises:
            RegionNotSupported: This method is only available for the Chinese region.
            ValueError: If the `login_ticket` argument is `None`, or if the `account_id` argument is `None`.
        """
        url = AUTH_URL.get_url(self.region) / "getMultiTokenByLoginTicket"
        login_ticket = login_ticket or self.cookies.get("login_ticket")
        account_id = account_id or self.account_id
        if login_ticket is None:
            raise ValueError("The 'login_ticket' argument cannot be None.")
        if account_id is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        params = {
            "login_ticket": login_ticket,
            "uid": account_id,
            "token_types": 3,
        }
        data = await self.request_lab(url, params=params)
        res_data = data["list"]
        for i in res_data:
            name = i.get("name")
            token = i.get("token")
            if name and token:
                self.cookies[name] = token
        stoken = self.cookies.get("stoken")
        stuid = self.cookies.get("stuid")
        if stoken and stuid:
            self.cookies["stuid"] = self.account_id
        return stoken

    async def get_cookie_token_by_stoken(
        self, stoken: Optional[str] = None, account_id: Optional[int] = None
    ) -> Optional[str]:
        """
        Retrieves a cookie token (`cookie_token`) using a super ticket (`stoken`).

        Args:
            stoken (Optional[str]): The super ticket to use to retrieve the cookie token. If not provided, the
                `stoken` cookie value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the cookie token. If not provided, the
                `account_id` attribute value will be used.

        Returns:
            Optional[str]: The retrieved cookie token (`cookie_token`).

        Raises:
            RegionNotSupported: This method is only available for the Chinese region.
            ValueError: If the `login_ticket` argument is `None`, or if the `account_id` argument is `None`.
        """
        stoken = stoken or self.cookies.get("stoken")
        account_id = account_id or self.account_id
        if stoken is None:
            raise ValueError("The 'stoken' argument cannot be None.")
        if account_id is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        url = PASSPORT_URL.get_url(self.region) / "getCookieAccountInfoBySToken"
        method = "GET" if self.region == Region.CHINESE else "POST"
        params = {
            "stoken": stoken,
            "uid": account_id,
        }
        data = await self.request_lab(url, method=method, params=params)
        cookie_token = data.get("cookie_token")
        if cookie_token:
            self.cookies["cookie_token"] = cookie_token
            self.cookies["account_id"] = self.account_id
        return cookie_token

    async def get_ltoken_by_stoken(
        self, stoken: Optional[str] = None, account_id: Optional[int] = None
    ) -> Optional[str]:
        """
        Retrieves a login token (`ltoken`) using a super ticket (`stoken`).

        Args:
            stoken (Optional[str]): The super ticket to use to retrieve the cookie token. If not provided, the
                `stoken` cookie value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the cookie token. If not provided, the
                `account_id` attribute value will be used.

        Returns:
            Optional[str]: The retrieved cookie token (`cookie_token`).

        Raises:
            RegionNotSupported: This method is only available for the Chinese region.
            ValueError: If the `login_ticket` argument is `None`, or if the `account_id` argument is `None`.
        """
        stoken = stoken or self.cookies.get("stoken")
        account_id = account_id or self.account_id
        if stoken is None:
            raise ValueError("The 'stoken' argument cannot be None.")
        if account_id is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        url = PASSPORT_URL.get_url(self.region) / "getLTokenBySToken"
        method = "GET" if self.region == Region.CHINESE else "POST"
        params = {
            "stoken": stoken,
            "uid": account_id,
        }
        data = await self.request_lab(url, method=method, params=params)
        ltoken = data.get("ltoken", "")
        if ltoken:
            self.cookies["ltoken"] = ltoken
            self.cookies["ltuid"] = self.account_id
        return ltoken

    async def get_authkey_by_stoken(self, game_biz: str, region: str, auth_appid: str) -> Optional[str]:
        """
        Get the auth key (`authkey`) for a game and region using a super ticket (`stoken`).

        Args:
            game_biz (str): The name of the game.
            region (str): The region in which the game is registered.
            auth_appid (str): The type of application for which the authkey is being requested.
                For example, to request wish records, use `webview_gacha`.

        Returns:
            Optional[str]: The authentication key, or None if not found.

        Raises:
            RegionNotSupported: This method is only available for the Chinese region.
            ValueError: If `stoken` is not found in the cookies or `player_id` not found.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported("This method is only available for the Chinese region.")
        stoken = self.cookies.get("stoken")
        if stoken is None:
            raise ValueError("stoken not found in cookies.")
        stuid = self.cookies.get("stuid")
        if stuid is None and self.account_id is None:
            raise ValueError("account_id or stuid not found")
        if self.account_id is not None and stuid is None:
            self.cookies.set("stuid", str(self.account_id))
        url = AUTH_KEY_URL.get_url(self.region)
        json = {
            "auth_appid": auth_appid,
            "game_biz": game_biz,
            "game_uid": self.player_id,
            "region": region,
        }
        data = await self.request_lab(url, data=json)
        return data.get("authkey")

    async def get_hk4e_token_by_cookie_token(
        self, game_biz: str, region: str, player_id: Optional[int] = None
    ) -> NoReturn:
        """
        Get HK4E token (`hk4e_token`) using cookie token (`cookie_token`).
        The resulting HK4E token will be automatically saved in self.cookies.

        Args:
            game_biz (str): The name of the game.
            region (str): The region in which the game is registered.
            player_id (Optional[int]): The player ID to use to retrieve the HK4E token. If not provided, the `player_id`
                attribute value will be used.

        Raises:
            ValueError: If `cookie_token` is not found in the cookies.
        """
        stoken = self.cookies.get("cookie_token")
        if stoken is None:
            raise ValueError("cookie_token not found in cookies.")
        url = HK4E_LOGIN_URL.get_url(self.region)
        json = {
            "game_biz": game_biz,
            "uid": self.player_id or player_id,
            "region": region,
            "lang": self.lang,
        }
        await self.request_api("POST", url=url, json=json)
