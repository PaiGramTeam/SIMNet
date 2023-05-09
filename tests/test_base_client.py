import pytest

from simnet.client.base import BaseClient
from simnet.client.cookies import Cookies


@pytest.mark.asyncio
class TestBaseClient:
    async def test_cookies(self):
        async with BaseClient(cookies={"uid": "114514"}) as client:
            assert isinstance(client.cookies, Cookies)
            client.cookies = {"account_id": "114514"}
            assert isinstance(client.cookies, Cookies)
            assert client.cookies.get("account_id") == "114514"
