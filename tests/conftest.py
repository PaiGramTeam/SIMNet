import asyncio
import os
import warnings

import pytest
import pytest_asyncio

from simnet.client.cookies import Cookies
from simnet.client.starrail import StarRailClient
from simnet.utils.cookies import parse_cookie
from simnet.utils.enum_ import Region


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
def player_id() -> int:  # skipcq: PY-D0003
    _player_id = os.environ.get("PLAYER_ID")
    if not _player_id:
        pytest.exit("No player id set", 1)
    return int(_player_id)


@pytest.fixture(scope="session")
def account_id() -> int:  # skipcq: PY-D0003
    _account_id = os.environ.get("ACCOUNT_ID")
    if not _account_id:
        pytest.exit("No player id set", 1)
    return int(_account_id)


@pytest_asyncio.fixture
async def starrail_client(  # skipcq: PY-D0003
    player_id: int, account_id: int, cookies: "Cookies"  # skipcq: PYL-W0621
):
    async with StarRailClient(
        player_id=player_id,
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance
