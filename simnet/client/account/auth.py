from typing import Optional, NoReturn

from simnet.client.base import BaseClient
from simnet.client.routes import (
    AUTH_URL,
    AUTH_KEY_URL,
    HK4E_LOGIN_URL,
    GET_COOKIES_TOKEN_BY_STOKEN_URL,
    GET_LTOKEN_BY_STOKEN_URL,
)
from simnet.utils.enum_ import Region


class AuthClient(BaseClient):
    """
    The AuthClient class is a client for authentication services.
    It is derived from the BaseClient class and provides methods for retrieving
    different authentication tokens and keys.
    """

    async def get_stoken_by_login_ticket(self) -> bool:
        """
        Retrieves a super ticket (`stoken`) using a login ticket (`login_ticket`) .

        Returns:
            bool: `True` if the super ticket successfully retrieved, otherwise `False`.

        Raises:
            ValueError: If `login_ticket` is not found in the cookies.
        """
        url = AUTH_URL.get_url(Region.CHINESE).join("getMultiTokenByLoginTicket")
        login_ticket = self.cookies.get("login_ticket")
        if login_ticket is None:
            raise ValueError("login_ticket not found in cookies.")
        params = {
            "login_ticket": login_ticket,
            "uid": self.account_id,
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
        if stoken:
            if stuid:
                self.cookies["stuid"] = self.account_id
            return True
        return False

    async def get_cookie_token_by_stoken(self) -> bool:
        """
        Retrieves a cookie token (`cookie_token`) using a super ticket (`stoken`).

        Returns:
            bool: `True` if the cookie token was successfully retrieved, otherwise `False`.

        Raises:
            ValueError: If `stoken` is not found in the cookies.
        """
        stoken = self.cookies.get("stoken")
        if stoken is None:
            raise ValueError("stoken not found in cookies.")
        url = GET_COOKIES_TOKEN_BY_STOKEN_URL.get_url(Region.CHINESE)
        params = {
            "stoken": stoken,
            "uid": self.account_id,
        }
        data = await self.request_lab(url, params=params)
        cookie_token = data.get("cookie_token", "")
        if cookie_token:
            self.cookies["cookie_token"] = cookie_token
            self.cookies["account_id"] = self.account_id
            return True
        return False

    async def get_ltoken_by_stoken(self) -> bool:
        """
        Retrieves a login token (`ltoken`) using a super ticket (`stoken`).

        Returns:
            bool: `True` if the login token was successfully retrieved, otherwise `False`.

        Raises:
            ValueError: If `stoken` is not found in the cookies.
        """
        stoken = self.cookies.get("stoken")
        if stoken is None:
            raise ValueError("stoken not found in cookies.")
        url = GET_LTOKEN_BY_STOKEN_URL.get_url(Region.CHINESE)
        params = {
            "stoken": stoken,
            "uid": self.account_id,
        }
        data = await self.request_lab(url, params=params)
        ltoken = data.get("ltoken", "")
        if ltoken:
            self.cookies["ltoken"] = ltoken
            self.cookies["ltuid"] = self.account_id
            return True
        return False

    async def get_authkey_by_stoken(self, game_biz: str, region: str, auth_appid: str) -> Optional[str]:
        """
        Get the auth key (`authkey`) for a game and region using a super ticket (`stoken`).

        Args:
            game_biz (str): The name of the game.
            region (str): The region in which the game is registered.
            auth_appid (str): The type of application for which the authkey is being requested.
                For example, to request wish records, use `webview_gacha`.

        Returns:
            str or None: The authentication key, or None if not found.

        Raises:
            ValueError: If `stoken` is not found in the cookies.
        """
        stoken = self.cookies.get("stoken")
        if stoken is None:
            raise ValueError("stoken not found in cookies.")
        url = AUTH_KEY_URL.get_url(self.region)
        json = {
            "auth_appid": auth_appid,
            "game_biz": game_biz,
            "game_uid": self.player_id,
            "region": region,
        }
        data = await self.request_lab(url, data=json)
        return data.get("authkey")

    async def get_hk4e_token_by_cookie_token(self, game_biz: str, region: str) -> NoReturn:
        """
        Get HK4E token (`hk4e_token`) using cookie token (`cookie_token`).
        The resulting HK4E token will be automatically saved in self.cookies.

        Args:
            game_biz (str): The name of the game.
            region (str): The region in which the game is registered.

        Raises:
            ValueError: If `cookie_token` is not found in the cookies.
        """
        stoken = self.cookies.get("cookie_token")
        if stoken is None:
            raise ValueError("cookie_token not found in cookies.")
        url = HK4E_LOGIN_URL.get_url(self.region)
        json = {
            "game_biz": game_biz,
            "uid": self.player_id,
            "region": region,
        }
        await self.request_lab(url, data=json)
