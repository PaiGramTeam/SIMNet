import json as jsonlib
import time
from typing import Optional

from simnet.client.components.auth_client import AuthBaseClient
from simnet.client.routes import GET_FP_URL
from simnet.utils.hex import get_random_hex_string_of_length

__all__ = ("AuthClient",)


class AuthClient(AuthBaseClient):
    """
    The AuthClient class is a client for authentication services.
    It is derived from the BaseClient class and provides methods for retrieving
    different authentication tokens and keys.
    """

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
