from typing import Optional

from simnet.client.base import BaseClient
from simnet.client.routes import HK4E_LOGIN_URL, PASSPORT_MA_URL, PASSPORT_URL
from simnet.utils.enums import Region
from simnet.utils.player import recognize_game_biz, recognize_server


class CookieTokenAuthClient(BaseClient):
    """Cookie token sub client for AuthClient."""

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
            url = PASSPORT_MA_URL.get_url(self.region) / "token/verifyCookieToken"
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
