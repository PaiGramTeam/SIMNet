from datetime import datetime
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet import GenshinClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def genshin_client(genshin_player_id: int, account_id: int, region: "Region", cookies: "Cookies"):
    if genshin_player_id is None:
        pytest.skip("Test case test_genshin_mi_creator skipped: No genshin player id set.")
    async with GenshinClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinMiCreatorClient:
    @staticmethod
    async def test_get_mi_creator_reward_history(genshin_client: "GenshinClient"):
        now = datetime.now()
        data = await genshin_client.get_mi_creator_reward_history(now.year, now.month)
        assert data.count >= 0

    @staticmethod
    async def test_get_mi_creator_reward_count(genshin_client: "GenshinClient"):
        data = await genshin_client.get_mi_creator_reward_count()
        assert len(data) >= 0
