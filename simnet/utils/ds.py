import hashlib
import json
import random
import string
import time
from enum import Enum
from typing import Any, Optional

from simnet.utils.enums import Region
from simnet.utils.types import QueryParamTypes

MIYOUSHE_VERSION = "2.69.1"
MIYOUSHE_APP_DS = "9XXf7BHajk1jwo3JAYncLjbYQizFEfoo"
MIYOUSHE_WEB_DS = "ZPDcG5oaYUGWVcrImzWLzBLYOX9LpYd7"


class DSType(Enum):
    """
    Enumeration of dynamic secret types.

    Attributes:
        WEB (str): Android dynamic secret type.
        ANDROID (str): Android dynamic secret type.
    """

    WEB = "web"
    ANDROID = "android"


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
    ds_type: Optional[DSType] = None,
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

    app_version = MIYOUSHE_VERSION
    client_type = "5"
    if region == Region.OVERSEAS:
        salt = "6s25p5ox5y14umn1p61aqyyvbvvl3lrt"
        app_version = "1.5.0"
    elif region == Region.CHINESE:
        if new_ds:
            if ds_type is None:
                salt = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
            elif ds_type == DSType.ANDROID:
                client_type = "2"
                salt = MIYOUSHE_APP_DS
            else:
                raise ValueError(f"Unknown ds_type: {ds_type}")
        else:
            if ds_type is None:
                salt = MIYOUSHE_WEB_DS
            elif ds_type == DSType.ANDROID:
                salt = "t0qEgfub6cvueAPgR5m9aQWWVciEer7v"
                client_type = "2"
            else:
                raise ValueError(f"Unknown ds_type: {ds_type}")
    else:
        raise ValueError(f"Unknown region: {region}")
    if new_ds:
        ds = new()
    else:
        ds = old()
    return app_version, client_type, ds
