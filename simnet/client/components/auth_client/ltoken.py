from typing import Optional

from simnet.client.base import BaseClient
from simnet.client.routes import PASSPORT_MA_URL, PASSPORT_URL
from simnet.utils.enums import Region


class LTokenAuthClient(BaseClient):
    """LToken sub client for AuthClient."""

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
            url = PASSPORT_MA_URL.get_url(self.region) / "token/verifyLToken"
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
