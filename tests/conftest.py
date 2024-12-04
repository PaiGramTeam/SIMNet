import asyncio
import os
import warnings
from pathlib import Path
from typing import Optional

import pytest
from dotenv import load_dotenv

from simnet.client.cookies import Cookies
from simnet.utils.cookies import parse_cookie
from simnet.utils.enums import Region

env_path = Path(".env")
if env_path.exists():
    load_dotenv()


@pytest.fixture(scope="session")
def event_loop():  # skipcq: PY-D0003
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        loop = asyncio.get_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def cookies() -> "Cookies":  # skipcq: PY-D0003
    cookies_str = os.environ.get("COOKIES")
    if not cookies_str:
        pytest.exit("No cookies set", 1)

    _cookies = Cookies(parse_cookie(cookies_str))
    if _cookies.account_id is None:
        warnings.warn(UserWarning("can not found account id in cookies"), stacklevel=2)

    return _cookies


@pytest.fixture(scope="session")
def starrail_cookies() -> Optional["Cookies"]:  # skipcq: PY-D0003
    cookies_str = os.environ.get("STARRAIL_COOKIES")
    if not cookies_str:
        return None
    _cookies = Cookies(parse_cookie(cookies_str))
    if _cookies.account_id is None:
        warnings.warn(UserWarning("can not found account id in starrail cookies"), stacklevel=2)

    return _cookies


@pytest.fixture(scope="session")
def zzz_cookies() -> Optional["Cookies"]:
    cookies_str = os.environ.get("ZZZ_COOKIES")
    if not cookies_str:
        return None
    _cookies = Cookies(parse_cookie(cookies_str))
    if _cookies.account_id is None:
        warnings.warn(UserWarning("can not found account id in zzz cookies"), stacklevel=2)

    return _cookies


@pytest.fixture(scope="session")
def genshin_player_id() -> Optional[int]:  # skipcq: PY-D0003
    _player_id = os.environ.get("GENSHIN_PLAYER_ID")
    if not _player_id:
        warnings.warn(UserWarning("No genshin player id set"), stacklevel=2)
        return None
    return int(_player_id)


@pytest.fixture(scope="session")
def starrail_player_id() -> Optional[int]:  # skipcq: PY-D0003
    _player_id = os.environ.get("STARRAIL_PLAYER_ID")
    if not _player_id:
        warnings.warn(UserWarning("No starrail player id set"), stacklevel=2)
        return None
    return int(_player_id)


@pytest.fixture(scope="session")
def zzz_player_id() -> Optional[int]:
    _player_id = os.environ.get("ZZZ_PLAYER_ID")
    if not _player_id:
        warnings.warn(UserWarning("No zzz player id set"), stacklevel=2)
        return None
    return int(_player_id)


@pytest.fixture(scope="session")
def account_id() -> Optional[int]:  # skipcq: PY-D0003
    _account_id = os.environ.get("ACCOUNT_ID")
    if not _account_id:
        return None
    return int(_account_id)


@pytest.fixture(scope="session")
def region() -> Region:  # skipcq: PY-D0003
    _region = os.environ.get("REGION")
    if not _region:
        return Region.CHINESE
    return Region(_region)


@pytest.fixture(scope="session")
def stoken() -> Optional[str]:  # skipcq: PY-D0003
    return os.environ.get("STOKEN")


@pytest.fixture(scope="session")
def login_ticket() -> Optional[str]:  # skipcq: PY-D0003
    return os.environ.get("LOGIN_TICKET")
