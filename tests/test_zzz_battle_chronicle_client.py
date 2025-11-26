from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.zzz import ZZZBattleChronicleClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def zzz_client(zzz_player_id: int, region: "Region", cookies: "Cookies", zzz_cookies: Optional["Cookies"]):
    if zzz_player_id is None:
        pytest.skip("Test case test_zzz_battle_chronicle_client skipped: No zzz player id set.")
    async with ZZZBattleChronicleClient(
        player_id=zzz_player_id,
        cookies=zzz_cookies or cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestZZZBattleChronicleClient:
    @staticmethod
    async def test_get_zzz_notes(zzz_client: "ZZZBattleChronicleClient"):
        notes = await zzz_client.get_zzz_notes()
        assert notes is not None

    @staticmethod
    async def test_get_zzz_notes_by_stoken(zzz_client: "ZZZBattleChronicleClient"):
        notes = await zzz_client.get_zzz_notes_by_stoken()
        assert notes is not None

    @staticmethod
    async def test_get_zzz_user(zzz_client: "ZZZBattleChronicleClient"):
        user_info = await zzz_client.get_zzz_user()
        assert user_info is not None

    @staticmethod
    async def test_get_zzz_abyss_abstract(zzz_client: "ZZZBattleChronicleClient"):
        abyss_abstract = await zzz_client.get_zzz_abyss_abstract()
        assert abyss_abstract is not None

    @staticmethod
    async def test_get_zzz_abysss2_abstract(zzz_client: "ZZZBattleChronicleClient"):
        abysss2_abstract = await zzz_client.get_zzz_abysss2_abstract()
        assert abysss2_abstract is not None

    @staticmethod
    async def test_get_zzz_characters(zzz_client: "ZZZBattleChronicleClient"):
        characters = await zzz_client.get_zzz_characters()
        assert characters is not None

    @staticmethod
    async def test_get_zzz_character_info(zzz_client: "ZZZBattleChronicleClient"):
        character_info = await zzz_client.get_zzz_character_info([1081, 1121])
        assert character_info is not None
        assert len(character_info.characters) == 2
        assert character_info.characters[0].id == 1081
        assert character_info.characters[1].id == 1121

    @staticmethod
    async def test_get_zzz_buddy_list(zzz_client: "ZZZBattleChronicleClient"):
        buddy_list = await zzz_client.get_zzz_buddy_list()
        assert buddy_list is not None

    @staticmethod
    async def test_get_zzz_challenge(zzz_client: "ZZZBattleChronicleClient"):
        challenge_list = await zzz_client.get_zzz_challenge()
        assert challenge_list is not None

    @staticmethod
    async def test_get_zzz_challenge_mem(zzz_client: "ZZZBattleChronicleClient"):
        challenge_list = await zzz_client.get_zzz_challenge_mem()
        assert challenge_list is not None

    @staticmethod
    async def test_get_zzz_cur_gacha_detail(zzz_client: "ZZZBattleChronicleClient"):
        gacha_detail = await zzz_client.get_zzz_cur_gacha_detail()
        assert gacha_detail is not None

    @staticmethod
    async def test_get_zzz_wish_history_by_hoyolab(zzz_client: "ZZZBattleChronicleClient"):
        gacha_detail = await zzz_client.get_wish_page_by_hoyolab(0, "GACHA_TYPE_PERMANENT")
        assert gacha_detail is not None
