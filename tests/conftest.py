import asyncio
import os
import warnings
from pathlib import Path

import pytest
from dotenv import load_dotenv

from simnet.client.cookies import Cookies
from simnet.utils.cookies import parse_cookie

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

    return _cookies


@pytest.fixture(scope="session")
def genshin_player_id() -> int:  # skipcq: PY-D0003
    _player_id = os.environ.get("GENSHIN_PLAYER_ID")
    if not _player_id:
        pytest.exit("No player id set", 1)
    return int(_player_id)


@pytest.fixture(scope="session")
def starrail_player_id() -> int:  # skipcq: PY-D0003
    _player_id = os.environ.get("STARRAIL_PLAYER_ID")
    if not _player_id:
        pytest.exit("No player id set", 1)
    return int(_player_id)


@pytest.fixture(scope="session")
def account_id() -> int:  # skipcq: PY-D0003
    _account_id = os.environ.get("ACCOUNT_ID")
    if not _account_id:
        pytest.exit("No player id set", 1)
    return int(_account_id)
