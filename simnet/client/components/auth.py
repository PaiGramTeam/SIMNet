import json
from typing import Optional, NoReturn, Tuple, Union

from simnet.client.base import BaseClient
from simnet.client.routes import (
    AUTH_URL,
    AUTH_KEY_URL,
    HK4E_LOGIN_URL,
    PASSPORT_URL,
    WEB_ACCOUNT_URL,
    QRCODE_URL,
    URL,
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
            self.cookies["stuid"] = str(self.account_id)
        return stoken

    async def get_cookie_token_by_login_ticket(self, login_ticket: Optional[str] = None) -> Optional[str]:
        """
        Retrieves a cookie token (`cookie_token`) using a login ticket (`login_ticket`).

        Args:
            login_ticket (Optional[str]): The login ticket to use to retrieve the cookie token. If not provided, the
                `login_ticket` cookie value will be used.

        Returns:
            Optional[str]: The retrieved cookie token (`cookie_token`).

        Raises:
            ValueError: If the `login_ticket` argument is `None`.
        """
        url = WEB_ACCOUNT_URL.get_url(self.region) / "cookie_accountinfo_by_loginticket"
        login_ticket = login_ticket or self.cookies.get("login_ticket")
        if login_ticket is None:
            raise ValueError("The 'login_ticket' argument cannot be None.")
        params = {"login_ticket": login_ticket}
        data = await self.request_lab(url, params=params)
        cookie_info = data.get("cookie_info")
        if not cookie_info:
            raise ValueError("The 'login_ticket' is expired.")
        account_id = cookie_info.get("account_id")
        cookie_token = cookie_info.get("cookie_token")
        if account_id:
            self.account_id = account_id
            self.cookies["account_id"] = str(account_id)
        if cookie_token:
            self.cookies["cookie_token"] = cookie_token
        return cookie_token

    def check_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> None:
        stoken = stoken or self.cookies.get("stoken")
        account_id = account_id or self.account_id
        mid = mid or self.cookies.get("mid")
        if stoken is None:
            raise ValueError("The 'stoken' argument cannot be None.")
        if account_id is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        if stoken.startswith("v2_"):
            if mid is None:
                raise ValueError("The 'mid' argument cannot be None.")
            self.cookies.set("mid", mid)
        self.cookies.set("stuid", str(account_id))
        self.cookies.set("stoken", stoken)

    async def get_cookie_token_by_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> Optional[str]:
        """
        Retrieves a cookie token (`cookie_token`) using a super ticket (`stoken`).

        Args:
            stoken (Optional[str]): The super ticket to use to retrieve the cookie token. If not provided, the
                `stoken` cookie value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the cookie token. If not provided, the
                `account_id` attribute value will be used.
            mid (Optional[str]): The machine ID to use to retrieve the cookie token. If not provided, the `mid`
                attribute value will be used.

        Returns:
            Optional[str]: The retrieved cookie token (`cookie_token`).

        Raises:
            ValueError: If the `login_ticket` argument is `None`, or if the `account_id` argument is `None`.
        """
        self.check_stoken(stoken, account_id, mid)
        url = PASSPORT_URL.get_url(self.region) / "getCookieAccountInfoBySToken"
        method = "GET" if self.region == Region.CHINESE else "POST"
        data = await self.request_lab(url, method=method)
        cookie_token = data.get("cookie_token")
        if cookie_token:
            self.cookies["cookie_token"] = cookie_token
            self.cookies["account_id"] = str(self.account_id)
        return cookie_token

    async def get_ltoken_by_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> Optional[str]:
        """
        Retrieves a login token (`ltoken`) using a super ticket (`stoken`).

        Args:
            stoken (Optional[str]): The super ticket to use to retrieve the cookie token. If not provided, the
                `stoken` cookie value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the cookie token. If not provided, the
                `account_id` attribute value will be used.
            mid (Optional[str]): The machine ID to use to retrieve the cookie token. If not provided, the `mid`
                attribute value will be used.

        Returns:
            Optional[str]: The retrieved cookie token (`cookie_token`).

        Raises:
            ValueError: If the `login_ticket` argument is `None`, or if the `account_id` argument is `None`.
        """
        self.check_stoken(stoken, account_id, mid)
        url = PASSPORT_URL.get_url(self.region) / "getLTokenBySToken"
        method = "GET" if self.region == Region.CHINESE else "POST"
        data = await self.request_lab(url, method=method)
        ltoken = data.get("ltoken", "")
        if ltoken:
            self.cookies["ltoken"] = ltoken
            self.cookies["ltuid"] = str(self.account_id)
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
            ValueError: If `stoken` is not found in the cookies or `player_id` not found.
        """
        self.check_stoken()
        url = AUTH_KEY_URL.get_url(self.region)
        json_ = {
            "auth_appid": auth_appid,
            "game_biz": game_biz,
            "game_uid": self.player_id,
            "region": region,
        }
        data = await self.request_lab(url, data=json_)
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
        json_ = {
            "game_biz": game_biz,
            "uid": self.player_id or player_id,
            "region": region,
            "lang": self.lang,
        }
        await self.request_api("POST", url=url, json=json_)

    async def gen_login_qrcode(
        self,
        app_id: str = "8",
    ) -> Tuple[str, str]:
        """
        Generate login qrcode and return url and ticket

        Args:
            app_id (str): The app id to use to generate the qrcode. If not provided, the `app_id` attribute value will be used.

        Returns:
            Tuple[str, str]: The url and ticket of the qrcode.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        data = {"app_id": app_id, "device": self.get_device_id()}
        res_json = await self.request_api("POST", url=QRCODE_URL / "fetch", json=data)
        url = res_json.get("url", "")
        if not url:
            return "", ""
        ticket = url.split("ticket=")[1]
        return url, ticket

    async def check_login_qrcode(self, ticket: str, app_id: str = "8") -> Union[bool, str]:
        """
        Check login qrcode and return token if success

        Args:
            ticket (str): The ticket of the qrcode.
            app_id (str): The app id to use to generate the qrcode. If not provided, the `app_id` attribute value will be used.

        Returns:
            Union[bool, str]: The token of the qrcode if success, else False.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        data = {"app_id": app_id, "ticket": ticket, "device": self.get_device_id()}
        res_data = await self.request_api("POST", url=QRCODE_URL / "query", json=data)
        if res_data.get("stat", "") != "Confirmed":
            return False
        info = json.loads(res_data.get("payload", {}).get("raw", "{}"))
        self.account_id = int(info.get("uid", 0))
        return info.get("token", "")

    async def accept_login_qrcode(self, url: str) -> None:
        """
        Accept login qrcode

        Args:
            url (str): The url of the qrcode.

        Returns:
            None
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        self.check_stoken()
        if not url.startswith("https://user.mihoyo.com/qr_code_in_game.html"):
            raise ValueError("Invalid url")
        u = URL(url)
        ticket = u.params.get("ticket")
        app_id = u.params.get("app_id")
        biz_key = u.params.get("biz_key")
        scan_url = (QRCODE_URL / "scan").replace("hk4e_cn", biz_key)
        data = {"ticket": ticket, "app_id": app_id, "device": self.get_device_id()}
        await self.request_lab(url=scan_url, data=data)
        game_token = await self.get_game_token_by_stoken()
        data["payload"] = {
            "proto": "Account",
            "raw": json.dumps({"uid": str(self.account_id), "token": game_token}, indent=4, ensure_ascii=False),
        }
        confirm_url = (QRCODE_URL / "confirm").replace("hk4e_cn", biz_key)
        await self.request_lab(url=confirm_url, data=data)

    async def get_stoken_v2_and_mid_by_game_token(self, game_token: str) -> Tuple[str, str]:
        """
        Get stoken_v2 and mid by game token

        Args:
            game_token (str): The game token to use to retrieve the stoken_v2 and mid.

        Returns:
            Tuple[str, str]: The stoken_v2 and mid.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        url = PASSPORT_URL.get_url(self.region) / "../../ma-cn-session/app/getTokenByGameToken"
        data = {
            "account_id": self.account_id,
            "game_token": game_token,
        }
        headers = {"x-rpc-app_id": "bll8iq97cem8" if self.region == Region.CHINESE else "c9oqaq3s3gu8"}
        data = await self.request_lab(url, data=data, headers=headers)
        mid = data.get("user_info", {}).get("mid", "")
        stoken_v2 = data.get("token", {}).get("token", "")
        self.cookies.set("mid", mid)
        self.cookies.set("stoken", stoken_v2)
        return stoken_v2, mid

    async def get_stoken_v2_and_mid_by_by_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
    ) -> Tuple[str, str]:
        """
        Get stoken_v2 and mid by stoken_v1

        Args:
            stoken (Optional[str]): The stoken_v1 to use to retrieve the stoken_v2 and mid. If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the stoken_v2 and mid. If not provided, the `account_id` attribute value will be used.

        Returns:
            Tuple[str, str]: The stoken_v2 and mid.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        self.check_stoken(stoken, account_id)
        url = PASSPORT_URL.get_url(self.region) / "../../ma-cn-session/app/getTokenBySToken"
        headers = {"x-rpc-app_id": "bll8iq97cem8"}
        data = await self.request_lab(url, method="POST", headers=headers)
        mid = data.get("user_info", {}).get("mid", "")
        stoken_v2 = data.get("token", {}).get("token", "")
        self.cookies.set("mid", mid)
        self.cookies.set("stoken", stoken_v2)
        return stoken_v2, mid

    async def get_game_token_by_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> str:
        """
        Get game token by stoken

        Args:
            stoken (Optional[str]): The stoken_v1 to use to retrieve the game token. If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the game token. If not provided, the `account_id` attribute value will be used.
            mid (Optional[str]): The mid to use to retrieve the game token. If not provided, the `mid` attribute value will be used.

        Returns:
            str: The game token.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        self.check_stoken(stoken, account_id, mid)
        url = AUTH_URL.get_url(self.region) / "getGameToken"
        data = await self.request_lab(url, method="GET")
        return data.get("game_token", "")
