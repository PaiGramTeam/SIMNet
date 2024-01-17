import json as jsonlib
import time
from typing import Optional, Tuple, Union

from simnet.client.base import BaseClient
from simnet.client.cookies import CookiesModel
from simnet.client.routes import (
    AUTH_URL,
    AUTH_KEY_URL,
    HK4E_LOGIN_URL,
    PASSPORT_URL,
    WEB_ACCOUNT_URL,
    QRCODE_URL,
    URL,
    GET_FP_URL,
)
from simnet.errors import RegionNotSupported
from simnet.utils.enums import Region
from simnet.utils.hex import get_random_hex_string_of_length
from simnet.utils.player import recognize_game_biz, recognize_server

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
        json = {
            "auth_appid": auth_appid,
            "game_biz": game_biz,
            "game_uid": self.player_id,
            "region": region,
        }
        data = await self.request_lab(url, data=json)
        return data.get("authkey")

    async def get_hk4e_token_by_cookie_token(
        self,
        game_biz: Optional[str] = None,
        region: Optional[str] = None,
        player_id: Optional[int] = None,
    ) -> None:
        """
        Get HK4E token (`hk4e_token`) using cookie token (`cookie_token`).
        The resulting HK4E token will be automatically saved in self.cookies.

        Args:
            game_biz (Optional[str]): The name of the game.
            region (Optional[str]): The region in which the game is registered.
            player_id (Optional[int]): The player ID to use to retrieve the HK4E token. If not provided, the `player_id`
                attribute value will be used.

        Raises:
            ValueError: If `cookie_token` is not found in the cookies.
        """
        cookie_token = self.cookies.get("cookie_token")
        if cookie_token is None:
            raise ValueError("cookie_token not found in cookies.")
        uid = self.player_id or player_id
        if not uid:
            raise ValueError("player_id not found.")
        game_biz = game_biz or recognize_game_biz(uid, self.game)
        region = region or recognize_server(uid, self.game)
        url = HK4E_LOGIN_URL.get_url(self.region)
        json = {
            "game_biz": game_biz,
            "uid": uid,
            "region": region,
            "lang": self.lang,
        }
        await self.request_api("POST", url=url, json=json)

    async def gen_login_qrcode(
        self,
        app_id: str = "8",
    ) -> Tuple[str, str]:
        """
        Generate login qrcode and return url and ticket

        Args:
            app_id (str): The app id to use to generate the qrcode.
                If not provided, the `app_id` attribute value will be used.

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
            app_id (str): The app id to use to generate the qrcode. If not provided,
                the `app_id` attribute value will be used.

        Returns:
            Union[bool, str]: The token of the qrcode if success, else False.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        data = {"app_id": app_id, "ticket": ticket, "device": self.get_device_id()}
        res_data = await self.request_api("POST", url=QRCODE_URL / "query", json=data)
        if res_data.get("stat", "") != "Confirmed":
            return False
        info = jsonlib.loads(res_data.get("payload", {}).get("raw", "{}"))
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
        raw = jsonlib.dumps({"uid": str(self.account_id), "token": game_token}, indent=4, ensure_ascii=False)
        data["payload"] = {
            "proto": "Account",
            "raw": raw,
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
        headers = {"x-rpc-app_id": "bll8iq97cem8"}
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
            stoken (Optional[str]): The stoken_v1 to use to retrieve the stoken_v2 and mid.
                If not provided, the `stoken` attribute value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the stoken_v2 and mid.
                If not provided, the `account_id` attribute value will be used.

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
        if self.region != Region.OVERSEAS:
            raise RegionNotSupported()
        self.check_stoken(stoken, account_id, mid)
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
        model = CookiesModel(mid=mid, stoken=token_map[1], ltoken=token_map[2], cookie_token=token_map[4])
        self.cookies.set("mid", model.mid)
        self.cookies.set("stoken", model.stoken)
        self.cookies.set("ltoken", model.ltoken)
        self.cookies.set("cookie_token", model.cookie_token)
        return model

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
        if self.region != Region.CHINESE:
            raise RegionNotSupported()
        self.check_stoken(stoken, account_id, mid)
        url = AUTH_URL.get_url(self.region) / "getGameToken"
        data = await self.request_lab(url, method="GET")
        return data.get("game_token", "")

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
            url = AUTH_KEY_URL.get_url(self.region) / "../../../account/ma-passport/token/verifySToken"
            headers = {"x-rpc-app_id": "c9oqaq3s3gu8"}
            await self.request_lab(url, method="POST", headers=headers)
        else:
            await self.get_cookie_token_by_stoken(stoken, account_id, mid)

    async def verify_ltoken(
        self,
        ltoken: Optional[str] = None,
        ltuid: Optional[int] = None,
    ) -> None:
        """
        Verify ltoken

        Args:
            ltoken (Optional[str]): The ltoken to use to verify.
                If not provided, the `ltoken` cookie value will be used.
            ltuid (Optional[int]): The account ID to use to verify.
                If not provided, the `ltuid` cookie value will be used.

        Returns:
            None

        Raises:
            ValueError: If the `ltoken` argument is `None`, or if the `account_id` argument is `None`.
            InvalidCookies: If the ltoken is invalid.
        """
        ltoken = ltoken or self.cookies.get("ltoken")
        ltuid = ltuid or self.account_id
        if ltoken is None:
            raise ValueError("The 'ltoken' argument cannot be None.")
        if ltuid is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        self.cookies.set("ltoken", ltoken)
        self.cookies.set("ltuid", str(ltuid))
        if self.region == Region.OVERSEAS:
            url = AUTH_KEY_URL.get_url(self.region) / "../../../account/ma-passport/token/verifyLToken"
            headers = {"x-rpc-app_id": "c9oqaq3s3gu8"}
            data = None
        else:
            url = PASSPORT_URL.get_url(self.region) / "getUserAccountInfoByLToken"
            headers = {"x-rpc-app_id": "bll8iq97cem8"}
            data = {
                "ltoken": ltoken,
                "uid": ltuid,
            }
        await self.request_lab(url, method="POST", headers=headers, data=data)

    async def verify_cookie_token(
        self,
        cookie_token: Optional[str] = None,
        account_id: Optional[int] = None,
    ) -> None:
        """
        Verify cookie token

        Args:
            cookie_token (Optional[str]): The cookie token to use to verify.
                If not provided, the `cookie_token` cookie value will be used.
            account_id (Optional[int]): The account ID to use to verify.
                If not provided, the `account_id` cookie value will be used.

        Returns:
            None

        Raises:
            ValueError: If the `cookie_token` argument is `None`, or if the `account_id` argument is `None`.
            InvalidCookies: If the cookie_token is invalid.
        """
        cookie_token = cookie_token or self.cookies.get("cookie_token")
        account_id = account_id or self.account_id
        if cookie_token is None:
            raise ValueError("The 'cookie_token' argument cannot be None.")
        if account_id is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        self.cookies.set("cookie_token", cookie_token)
        self.cookies.set("account_id", str(account_id))
        if self.region == Region.OVERSEAS:
            url = AUTH_KEY_URL.get_url(self.region) / "../../../account/ma-passport/token/verifyCookieToken"
            headers = {"x-rpc-app_id": "c9oqaq3s3gu8"}
            data = None
        else:
            url = PASSPORT_URL.get_url(self.region) / "getUserAccountInfoByCookieToken"
            headers = {"x-rpc-app_id": "bll8iq97cem8"}
            data = {
                "cookie_token": cookie_token,
                "uid": account_id,
            }
        await self.request_lab(url, method="POST", headers=headers, data=data)

    async def get_fp(
        self,
        device_id: Optional[str] = None,
        device_fp: Optional[str] = None,
        extend_properties: Optional[dict] = None,
        app_name: str = "bbs_cn",
        platform: int = 2,
    ) -> str:
        """
        Get Device Fingerprint

        Args:
            device_id (Optional[str]): Device ID, if not provided, use `get_device_id()`.
            device_fp (Optional[int]): Device fingerprint, if not provided, use `get_device_fp()`.
            extend_properties (Optional[dict]): Device extension information,
                defaults to auto-generated if not provided.
            app_name (str): APP name, defaults to "bbs_cn" if not provided.
            platform (int): Device platform code, same as client_type in the DS algorithm.

        Returns:
            str: The device fingerprint.
        """
        seed_time = int(time.time() * 1000)
        seed_id = get_random_hex_string_of_length(13)
        if extend_properties is None:
            model = get_random_hex_string_of_length(6)
            extend_properties = {
                "cpuType": "arm64-v8a",
                "romCapacity": "512",
                "productName": model,
                "romRemain": "256",
                "manufacturer": "XiaoMi",
                "appMemory": "512",
                "hostname": "dg02-pool03-kvm87",
                "screenSize": "1080x1920",
                "osVersion": "13",
                "vendor": "中国移动",
                "accelerometer": "1.4883357x7.1712894x6.2847486",
                "buildTags": "release-keys",
                "model": model,
                "brand": "XiaoMi",
                "oaid": "",
                "hardware": "qcom",
                "deviceType": "OP5913L1",
                "devId": "REL",
                "serialNumber": "unknown",
                "buildTime": "1687848011000",
                "buildUser": "root",
                "ramCapacity": "469679",
                "magnetometer": "20.081251x-27.487501x2.1937501",
                "display": f"{model}_13.1.0.181(CN01)",
                "ramRemain": "215344",
                "deviceInfo": f"XiaoMi/{model}/OP5913L1:13/SKQ1.221119.001/T.118e6c7-5aa23-73911:user/release-keys",
                "gyroscope": "0.030226856x0.014647375x0.010652636",
                "vaid": "",
                "buildType": "user",
                "sdkVersion": "33",
                "board": "taro",
            }
        ext_fields = jsonlib.dumps(extend_properties)
        data = {
            "app_name": app_name,
            "device_fp": device_fp or self.get_device_fp(),
            "device_id": device_id or self.get_device_fp(),
            "ext_fields": ext_fields,
            "platform": platform,
            "seed_id": seed_id,
            "seed_time": seed_time,
        }
        new_device_fp = await self.request_lab(GET_FP_URL, method="POST", data=data)
        self.device_fp = new_device_fp
        return new_device_fp
