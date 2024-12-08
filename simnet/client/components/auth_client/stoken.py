import json
from typing import Optional

from simnet.client.base import BaseClient
from simnet.client.cookies import CookiesModel
from simnet.client.routes import AUTH_KEY_URL, AUTH_URL, PASSPORT_MA_URL, PASSPORT_URL, QRCODE_URL, URL
from simnet.utils.enums import Region
from simnet.utils.player import recognize_game_biz, recognize_server


class StokenAuthClient(BaseClient):
    """Stoken sub client for AuthClient."""

    def check_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> None:
        """
        Checks and sets the stoken, account_id, and mid for a user.

        This function retrieves the stoken, account_id, and mid from the provided arguments
        or falls back to using existing properties/cookies. It then validates the presence of
        'stoken' and 'account_id'. If the stoken starts with 'v2_', the presence of 'mid' is
        also validated. Finally, the stoken, account_id, and potentially the mid are set to
        the cookies.

        Args:
            stoken (str, optional): The stoken to check and set. Defaults to the stoken cookie.
            account_id (int, optional): The account ID to check and set. Defaults to self.account_id.
            mid (str, optional): The mid to check and set. Defaults to the mid cookie.

        Raises:
            ValueError: If the stoken, account_id, or mid (when stoken starts with 'v2_') is not provided.

        Returns:
            None: This function modifies instance properties and does not return a value.
        """
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

    async def get_authkey_by_stoken(
        self,
        auth_appid: str,
        game_biz: Optional[str] = None,
        region: Optional[str] = None,
    ) -> Optional[str]:
        """
        Get the auth key (`authkey`) for a game and region using a super ticket (`stoken`).

        Args:
            auth_appid (str): The type of application for which the authkey is being requested.
                For example, to request wish records, use `webview_gacha`.
            game_biz (Optional[str]): The name of the game.
            region (Optional[str]): The region in which the game is registered.

        Returns:
            Optional[str]: The authentication key, or None if not found.

        Raises:
            ValueError: If `stoken` is not found in the cookies or `player_id` not found.
        """
        self.check_stoken()
        if not self.player_id:
            raise ValueError("player_id not found.")
        game_biz = game_biz or recognize_game_biz(self.player_id, self.game)
        region = region or recognize_server(self.player_id, self.game)
        url = AUTH_KEY_URL.get_url(self.region)
        json_data = {
            "auth_appid": auth_appid,
            "game_biz": game_biz,
            "game_uid": self.player_id,
            "region": region,
        }
        data = await self.request_lab(url, data=json_data)
        return data.get("authkey")

    async def get_stoken_v2_and_mid_by_by_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
    ) -> tuple[str, str]:
        """
        Get stoken_v2 and mid by stoken_v1

        Args:
            stoken (Optional[str]): The stoken_v1 to use to retrieve the stoken_v2 and mid.
                If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the stoken_v2 and mid.
                If not provided, the `account_id` attribute value will be used.

        Returns:
            Tuple[str, str]: The stoken_v2 and mid.
        """
        self.region_specific(True)
        self.check_stoken(stoken, account_id)
        url = PASSPORT_MA_URL.get_url(self.region) / "app/getTokenBySToken"
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
            stoken (Optional[str]): The stoken_v1 to use to retrieve the game token.
                If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the game token.
                If not provided, the `account_id` attribute value will be used.
            mid (Optional[str]): The mid to use to retrieve the game token.
                If not provided, the `mid` attribute value will be used.

        Returns:
            str: The game token.
        """
        self.region_specific(True)
        self.check_stoken(stoken, account_id, mid)
        url = AUTH_URL.get_url(self.region) / "getGameToken"
        data = await self.request_lab(url, method="GET")
        return data.get("game_token", "")

    async def get_all_token_by_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> CookiesModel:
        """
        Get stoken_v2, mid, ltoken and cookie_token by stoken v1 or v2

        Args:
            stoken (Optional[str]): The stoken_v1 to use to retrieve the stoken_v2 and mid.
                If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the stoken_v2 and mid.
                If not provided, the `account_id` attribute value will be used.
            mid (Optional[str]): The mid to use to retrieve the stoken_v2 and mid.

        Returns:
            CookiesModel: The stoken_v2, mid, ltoken and cookie_token.
        """
        self.region_specific(False)
        self.check_stoken(stoken, account_id, mid)
        account_id = account_id or self.account_id
        url = AUTH_KEY_URL.get_url(self.region) / "../../../account/ma-passport/token/getBySToken"
        headers = {"x-rpc-app_id": "c9oqaq3s3gu8"}
        data_ = {"dst_token_types": [1, 2, 4]}
        data = await self.request_lab(url, method="POST", headers=headers, data=data_)
        tokens = data.get("tokens", [])
        token_map = {1: "", 2: "", 4: ""}
        for token in tokens:
            token_type = token.get("token_type", 0)
            token_map[token_type] = token.get("token", "")
        mid = data.get("user_info", {}).get("mid", "")
        model = CookiesModel(stoken=token_map[1])
        ltoken, cookie_token = token_map[2], token_map[4]
        if ltoken.startswith("v2_"):
            model.ltoken_v2 = ltoken
        else:
            model.ltoken = ltoken
        if cookie_token.startswith("v2_"):
            model.cookie_token_v2 = cookie_token
        else:
            model.cookie_token = cookie_token
        model.set_mid(mid)
        model.set_uid(account_id)
        model.set_v2_uid(account_id)

        self.cookies.set("mid", model.mid)
        self.cookies.set("stoken", model.stoken)
        if model.ltoken:
            self.cookies.set("ltoken", model.ltoken)
        if model.ltoken_v2:
            self.cookies.set("ltoken_v2", model.ltoken_v2)
            self.cookies.set("ltmid_v2", model.ltmid_v2)
        if model.cookie_token:
            self.cookies.set("cookie_token", model.cookie_token)
        if model.cookie_token_v2:
            self.cookies.set("cookie_token_v2", model.cookie_token_v2)
            self.cookies.set("account_mid_v2", model.account_mid_v2)
        return model

    async def accept_login_qrcode(self, url: str) -> None:
        """
        Accept login qrcode

        Args:
            url (str): The url of the qrcode.

        Returns:
            None
        """
        self.region_specific(True)
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
        raw = json.dumps(
            {"uid": str(self.account_id), "token": game_token},
            indent=4,
            ensure_ascii=False,
        )
        data["payload"] = {
            "proto": "Account",
            "raw": raw,
        }
        confirm_url = (QRCODE_URL / "confirm").replace("hk4e_cn", biz_key)
        await self.request_lab(url=confirm_url, data=data)

    async def verify_stoken(
        self,
        stoken: Optional[str] = None,
        account_id: Optional[int] = None,
        mid: Optional[str] = None,
    ) -> None:
        """
        Verify stoken

        Args:
            stoken (Optional[str]): The stoken_v1 to use to retrieve the stoken_v2 and mid.
                If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the stoken_v2 and mid.
                If not provided, the `account_id` attribute value will be used.
            mid (Optional[str]): The mid to use to retrieve the stoken_v2 and mid.

        Returns:
            None

        Raises:
            ValueError: If the `stoken` argument is `None`, or if the `account_id` argument is `None`.
            InvalidCookies: If the stoken is invalid.
        """
        self.check_stoken(stoken, account_id, mid)
        if self.region == Region.OVERSEAS:
            url = PASSPORT_MA_URL.get_url(self.region) / "token/verifySToken"
            headers = {"x-rpc-app_id": "c9oqaq3s3gu8"}
            await self.request_lab(url, method="POST", headers=headers)
        else:
            await self.get_cookie_token_by_stoken(stoken, account_id, mid)
