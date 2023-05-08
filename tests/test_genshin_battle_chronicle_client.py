from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.models.genshin.chronicle.stats import FullGenshinUserStats, Stats
from simnet.utils.enum_ import Region

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def genshin_client(genshin_player_id: int, account_id: int, cookies: "Cookies"):
    async with GenshinBattleChronicleClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinBattleChronicleClient:
    async def test_get_battle_chronicle(
        self, genshin_client: GenshinBattleChronicleClient
    ):
        user = await genshin_client.get_genshin_user()
        assert user.stats.days_active >= 0

    async def test_get_full_genshin_user(
        self, genshin_client: GenshinBattleChronicleClient
    ):
        user = await genshin_client.get_full_genshin_user()
        assert isinstance(user, FullGenshinUserStats)
        assert isinstance(user.stats, Stats)

    async def test_get_partial_genshin_user(
        self, genshin_client: GenshinBattleChronicleClient
    ):
        user = await genshin_client.get_partial_genshin_user()
        assert user.stats.days_active >= 0
