import hashlib
import json
import random
import string
import time
from enum import Enum
from typing import Any, Optional, Dict

from simnet.utils.enum_ import Region
from simnet.utils.types import QueryParamTypes


class DSType(Enum):
    """
    Enumeration of dynamic secret types.

    Attributes:
        WEB (str): The web dynamic secret type.
        ANDROID_WEB (str): The Android web dynamic secret type.
    """

    WEB = "web"
    ANDROID_WEB = "android_web"


DS_VERSION: Dict[Region, str] = {
    Region.OVERSEAS: "1.5.0",
    Region.CHINESE: "2.49.1",
}
DS_CLIENT_TYPE: Dict[Region, Dict[DSType, str]] = {
    Region.OVERSEAS: {
        DSType.ANDROID_WEB: "5",
    },
    Region.CHINESE: {
        DSType.WEB: "2",
        DSType.ANDROID_WEB: "5",
    },
}
DS_SALT: Dict[Region, Dict[DSType, str]] = {
    Region.OVERSEAS: {
        DSType.ANDROID_WEB: "6s25p5ox5y14umn1p61aqyyvbvvl3lrt",
    },
    Region.CHINESE: {
        DSType.ANDROID_WEB: "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs",
        DSType.WEB: "DG8lqMyc9gquwAUFc7zBS62ijQRX9XF7",
    },
}


def hex_digest(text):
    """
    Computes the MD5 hash digest of the given text.

    Args:
        text (str): The text to hash.

    Returns:
        str: The MD5 hash digest of the given text.
    """
    _md5 = hashlib.md5()  # nosec B303
    _md5.update(text.encode())
    return _md5.hexdigest()


def generate_dynamic_secret(
    region: Region,
    ds_type: Optional[DSType] = DSType.WEB,
    new_ds: bool = False,
    data: Any = None,
    params: Optional[QueryParamTypes] = None,
):
    """
    Generates a dynamic secret.

    Args:
        region (Region): The region for which to generate the dynamic secret.
        ds_type (Optional[DSType], optional): The dynamic secret type. Defaults to None.
        new_ds (bool, optional): Whether to generate a new or old dynamic secret. Defaults to False.
        data (Any, optional): The data to include in the dynamic secret. Defaults to None.
        params (Optional[QueryParamTypes], optional): The query parameters to include in the dynamic secret.
            Defaults to None.

    Raises:
        ValueError: If the region or ds_type is not recognized.

    Returns:
        Tuple[str, str, str]: A tuple containing the app version, client type, and dynamic secret.
    """

    def new():
        """Create a new dynamic secret 2."""
        t = str(int(time.time()))
        r = str(random.randint(100001, 200000))  # nosec
        b = json.dumps(data) if data else ""
        q = "&".join(f"{k}={v}" for k, v in sorted(params.items())) if params else ""
        c = hex_digest(f"salt={salt}&t={t}&r={r}&b={b}&q={q}")
        return f"{t},{r},{c}"

    def old():
        """Create a new dynamic secret."""
        t = str(int(time.time()))
        r = "".join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = hex_digest(f"salt={salt}&t={t}&r={r}")
        return f"{t},{r},{c}"

    app_version = DS_VERSION[region]
    ds_type = ds_type or DSType.ANDROID_WEB
    client_type = DS_CLIENT_TYPE[region][ds_type]
    salt = DS_SALT[region][ds_type]
    new_ds = new_ds or (Region.CHINESE and ds_type == DSType.ANDROID_WEB)
    if new_ds:
        ds = new()
    else:
        ds = old()
    return app_version, client_type, ds
