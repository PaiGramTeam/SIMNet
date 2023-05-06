import asyncio
import os
import warnings

import pytest
import pytest_asyncio

from pathlib import Path

from simnet.client.starrail import StarRailClient
from simnet.utils.enum_ import Region

env_path = Path(".env")
if env_path.exists():
    from dotenv import load_dotenv

    load_dotenv()


@pytest.fixture(scope="session")
def event_loop():  # skipcq: PY-D0003
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        loop = asyncio.get_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def cookies() -> str:  # skipcq: PY-D0003
    cookies_str = os.environ.get("COOKIES")
    if not cookies_str:
        pytest.exit("No cookies set", 1)
    return cookies_str


@pytest_asyncio.fixture
async def starrail_client(  # skipcq: PY-D0003
    cookies: str  # skipcq: PYL-W0621
):
    async with StarRailClient(
        cookies=cookies,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance
