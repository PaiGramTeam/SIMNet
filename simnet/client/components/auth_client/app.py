import json
from typing import TYPE_CHECKING, Union

from simnet.client.base import BaseClient
from simnet.client.routes import PASSPORT_CN_URL, QRCODE_URL
from simnet.utils.constants import APP_CLOUD_IDS

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


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

    async def check_login_qrcode(self, ticket: str, app_id: str = "8") -> Union[dict, "Cookies"]:
        """
        Check QR code login status and retrieve user authentication information

        This method verifies the validity of a QR code login ticket and obtains user account information
        after successful scanning confirmation. It makes an API request to query the QR code status,
        and if confirmed, parses the returned user data.

        Args:
            ticket (str): QR code ticket identifier used to validate a specific QR code session
            app_id (str, optional): Application ID, defaults to "8". Used to identify the source application

        Returns:
            tuple: A tuple containing:
                - info (dict): User authentication information dictionary with uid and other user data
                - cookies (http.cookies.SimpleCookie): Client session cookies for maintaining login state
            bool: Returns False if the QR code is not confirmed or validation fails

        Raises:
            May raise network request related exceptions, handled by the underlying client
        """
        self.region_specific(True)
        data = {"app_id": app_id, "ticket": ticket, "device": self.get_device_id()}
        headers = {
            "x-rpc-device_fp": self.get_device_fp(),
            "x-rpc-device_id": self.get_device_id(),
        }
        async with AppAuthClient() as client:
            res_data = await client.request_api("POST", url=QRCODE_URL / "query", json=data, headers=headers)
        if res_data.get("stat", "") != "Confirmed":
            return False
        info = json.loads(res_data.get("payload", {}).get("raw", "{}"))
        self.account_id = int(info.get("uid", 0))
        return info, client.cookies

    async def gen_login_qrcode_v2(self, app_id: str = "8") -> tuple[str, str]:
        """
        Generate login qrcode and return url and ticket

        Args:
            app_id (str): The app id to use to generate the qrcode.
                If not provided, the `app_id` attribute value will be used.

        Returns:
            Tuple[str, str]: The url and ticket of the qrcode.
        """
        self.region_specific(True)
        url = PASSPORT_CN_URL / "web/createQRLogin"
        headers = {
            "x-rpc-app_id": APP_CLOUD_IDS[str(app_id)],
            "x-rpc-client_type": "22",
            "x-rpc-device_fp": self.get_device_fp(),
            "x-rpc-device_id": self.get_device_id(),
            "x-rpc-device_name": self.device_name,
        }
        res_data = await self.request_api("POST", url=url, headers=headers)
        return res_data["url"], res_data["ticket"]

    async def check_login_qrcode_v2(self, ticket: str, app_id: str = "8") -> Union[dict, "Cookies"]:
        """
        Check QR code login status and retrieve user authentication information

        This method verifies the validity of a QR code login ticket and obtains user account information
        after successful scanning confirmation. It makes an API request to query the QR code status,
        and if confirmed, parses the returned user data.

        Args:
            ticket (str): QR code ticket identifier used to validate a specific QR code session
            app_id (str, optional): Application ID, defaults to "8". Used to identify the source application

        Returns:
            tuple: A tuple containing:
                - info (dict): User authentication information dictionary with uid and other user data
                - cookies (http.cookies.SimpleCookie): Client session cookies for maintaining login state
            bool: Returns False if the QR code is not confirmed or validation fails

        Raises:
            May raise network request related exceptions, handled by the underlying client
        """
        self.region_specific(True)
        url = PASSPORT_CN_URL / "web/queryQRLoginStatus"
        headers = {
            "x-rpc-app_id": APP_CLOUD_IDS[str(app_id)],
            "x-rpc-client_type": "22",
            "x-rpc-device_fp": self.get_device_fp(),
            "x-rpc-device_id": self.get_device_id(),
            "x-rpc-device_name": self.device_name,
        }
        json_data = {
            "ticket": ticket,
        }
        async with AppAuthClient() as client:
            res_data = await client.request_api("POST", url=url, json=json_data, headers=headers)
        if res_data.get("status", "") != "Confirmed":
            return False
        return res_data, client.cookies
