import json
from typing import Union

from simnet.client.base import BaseClient
from simnet.client.routes import QRCODE_URL


class AppAuthClient(BaseClient):
    """App sub client for AuthClient."""

    async def gen_login_qrcode(
        self,
        app_id: str = "8",
    ) -> tuple[str, str]:
        """
        Generate login qrcode and return url and ticket

        Args:
            app_id (str): The app id to use to generate the qrcode.
                If not provided, the `app_id` attribute value will be used.

        Returns:
            Tuple[str, str]: The url and ticket of the qrcode.
        """
        self.region_specific(True)
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
        self.region_specific(True)
        data = {"app_id": app_id, "ticket": ticket, "device": self.get_device_id()}
        res_data = await self.request_api("POST", url=QRCODE_URL / "query", json=data)
        if res_data.get("stat", "") != "Confirmed":
            return False
        info = json.loads(res_data.get("payload", {}).get("raw", "{}"))
        self.account_id = int(info.get("uid", 0))
        return info.get("token", "")
