from typing import Optional

from simnet.client.base import BaseClient
from simnet.client.routes import AUTH_URL, WEB_ACCOUNT_URL


class LoginTicketAuthClient(BaseClient):
    """Login ticket sub client for AuthClient."""

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
