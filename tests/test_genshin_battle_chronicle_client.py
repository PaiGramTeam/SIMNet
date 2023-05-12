from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.models.genshin.chronicle.stats import FullGenshinUserStats, Stats

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enum_ import Region


@pytest_asyncio.fixture
async def genshin_client(genshin_player_id: int, account_id: int, region: "Region", cookies: "Cookies"):
    async with GenshinBattleChronicleClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinBattleChronicleClient:
    @staticmethod
    async def test_get_battle_chronicle(genshin_client: GenshinBattleChronicleClient):
        user = await genshin_client.get_genshin_user()
        assert user.stats.days_active >= 0

    @staticmethod
    async def test_get_full_genshin_user(genshin_client: GenshinBattleChronicleClient):
        user = await genshin_client.get_full_genshin_user()
        assert isinstance(user, FullGenshinUserStats)
        assert isinstance(user.stats, Stats)

    @staticmethod
    async def test_get_partial_genshin_user(
        genshin_client: GenshinBattleChronicleClient,
    ):
        user = await genshin_client.get_partial_genshin_user()
        assert user.stats.days_active >= 0

    @staticmethod
    async def test_get_genshin_characters(
        genshin_client: GenshinBattleChronicleClient,
    ):
        characters = await genshin_client.get_genshin_characters()
        assert len(characters) > 0
        for character in characters:
            assert character.id
            assert character.level
