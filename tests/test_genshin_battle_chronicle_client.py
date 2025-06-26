from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.models.genshin.chronicle.stats import FullGenshinUserStats, Stats

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def genshin_client(genshin_player_id: int, region: "Region", cookies: "Cookies"):
    if genshin_player_id is None:
        pytest.skip("Test case test_genshin_battle_chronicle_client skipped: No genshin player id set.")
    async with GenshinBattleChronicleClient(
        player_id=genshin_player_id,
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinBattleChronicleClient:
    @staticmethod
    async def test_get_partial_genshin_user(genshin_client: GenshinBattleChronicleClient):
        user = await genshin_client.get_partial_genshin_user()
        assert user.stats.days_active >= 0

    @staticmethod
    async def test_get_genshin_characters(genshin_client: GenshinBattleChronicleClient):
        characters = await genshin_client.get_genshin_characters()
        assert len(characters) > 0
        for character in characters:
            assert character.id
            assert character.level

    @staticmethod
    async def test_get_battle_chronicle(genshin_client: GenshinBattleChronicleClient):
        user = await genshin_client.get_genshin_user()
        assert user.stats.days_active >= 0

    @staticmethod
    async def test_get_genshin_spiral_abyss(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_spiral_abyss()
        assert data

    @staticmethod
    async def test_get_genshin_imaginarium_theater(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_imaginarium_theater()
        assert len(data.data) > 0

    @staticmethod
    async def test_get_genshin_hard_challenge(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_hard_challenge()
        assert len(data.data) > 0

    @staticmethod
    async def test_get_genshin_notes(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_notes()
        assert data

    @staticmethod
    async def test_get_full_genshin_user(genshin_client: GenshinBattleChronicleClient):
        user = await genshin_client.get_full_genshin_user()
        assert isinstance(user, FullGenshinUserStats)
        assert isinstance(user.stats, Stats)

    @staticmethod
    async def test_get_genshin_activities(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_activities()
        assert data

    @staticmethod
    async def test_get_genshin_notes_by_stoken(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_notes_by_stoken()
        assert data

    @staticmethod
    async def test_get_genshin_character_list(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_character_list()
        assert len(data) > 0

    @staticmethod
    async def test_get_genshin_character_detail(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_character_detail([10000021])
        assert data
        assert len(data.characters) > 0
        assert data.characters[0].base.id == 10000021

    @staticmethod
    async def test_get_genshin_achievement_info(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_achievement_info()
        assert data

    @staticmethod
    async def test_get_genshin_act_calendar(genshin_client: GenshinBattleChronicleClient):
        data = await genshin_client.get_genshin_act_calendar()
        assert data
