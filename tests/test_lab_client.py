from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.lab import LabClient
from simnet.utils.enum_ import Region, Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def client_instance(account_id: int, cookies: "Cookies"):
    async with LabClient(
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestStarRailClient:
    @staticmethod
    async def test_get_user_info(account_id: int, client_instance: "LabClient"):
        user_info = await client_instance.get_user_info()
        assert user_info.nickname
        assert user_info.accident_id == account_id

    @staticmethod
    async def test_get_genshin_accounts(client_instance: "LabClient"):
        genshin_accounts = await client_instance.get_genshin_accounts()
        for genshin_account in genshin_accounts:
            assert genshin_account.game == Game.GENSHIN
            assert len(str(genshin_account.uid)) == 9
