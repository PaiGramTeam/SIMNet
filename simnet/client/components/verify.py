import json
import re
import time
from typing import Optional

from httpx import Headers

from simnet.client.base import BaseClient
from simnet.client.routes import URL
from simnet.errors import RegionNotSupported
from simnet.utils.enums import Region


class VerifyClient(BaseClient):
    """VerifyClient component."""

    HOST = URL("https://api-takumi-record.mihoyo.com")
    VERIFICATION_HOST = URL("https://api.geetest.com")
    CREATE_VERIFICATION_URL = HOST / "/game_record/app/card/wapi/createVerification"
    VERIFY_VERIFICATION_URL = HOST / "/game_record/app/card/wapi/verifyVerification"
    AJAX_URL = VERIFICATION_HOST / "/ajax.php"

    async def create_verification(self, is_high: bool = False):
        """Create a verification challenge.

        Args:
            is_high (bool): Ifs the challenge for a high risk device.

        Returns:
            str: The challenge.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported("This method is only available for the Chinese region.")
        params = {"is_high": "true" if is_high else "false"}
        return await self.request_lab(self.CREATE_VERIFICATION_URL, params=params)

    async def verify_verification(self, challenge: str, validate: str):
        """Verify a verification challenge.

        Args:
            challenge (str): The challenge code.
            validate (str): The validate code.

        Returns:
            str: The verification result.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported("This method is only available for the Chinese region.")
        data = {"geetest_challenge": challenge, "geetest_validate": validate, "geetest_seccode": f"{validate}|jordan"}
        return await self.request_lab(self.VERIFY_VERIFICATION_URL, data=data)

    async def request_verify_ajax(self, referer: str, gt: str, challenge: str) -> Optional[str]:
        """Get the ajax validate code.

        Args:
            referer (str): The web referer.
            gt (str): The gt challenge.
            challenge (str): The challenge code.

        Returns:
            Optional[str]: The ajax validate code.
        """
        if self.region != Region.CHINESE:
            raise RegionNotSupported("This method is only available for the Chinese region.")
        params = {
            "gt": gt,
            "challenge": challenge,
            "lang": "zh-cn",
            "pt": 3,
            "client_type": "web_mobile",
            "callback": f"geetest_{int(time.time() * 1000)}",
        }
        headers = Headers()
        headers["user-agent"] = self.user_agent
        headers["x-rpc-app_version"] = self.app_version
        headers["x-rpc-client_type"] = self.client_type
        headers["x-rpc-device_id"] = self.get_device_id()
        headers["x-rpc-device_fp"] = self.get_device_fp()
        headers["referer"] = referer
        response = await self.request("GET", self.AJAX_URL, params=params, headers=headers)
        text = response.text
        json_data = re.findall(r"^.*?\((\{.*?)\)$", text)[0]
        data = json.loads(json_data)
        if "success" in data["status"] and "success" in data["data"]["result"]:
            return data["data"]["validate"]
        return None
