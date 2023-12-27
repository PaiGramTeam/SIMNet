from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.errors import NeedChallenge

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def starrail_client(starrail_player_id: int, account_id: int, region: "Region", cookies: "Cookies"):
    if starrail_player_id is None:
        pytest.skip("Test case test_genshin_calculator_client skipped: No starrail player id set.")
    async with StarRailBattleChronicleClient(
        player_id=starrail_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestStarrailBattleChronicleClient:
    @staticmethod
    async def test_get_starrail_user(starrail_client: "StarRailBattleChronicleClient"):
        user = await starrail_client.get_starrail_user()
        assert user is not None
        assert user.stats.chest_num > 0
        assert len(user.characters) > 0
        character = user.characters[-1]
        assert character.id > 0

    @staticmethod
    @pytest.mark.xfail(raises=NeedChallenge, reason="Challenge is needed, but not implemented yet.")
    async def test_get_starrail_notes(starrail_client: "StarRailBattleChronicleClient"):
        notes = await starrail_client.get_starrail_notes()
        assert notes is not None

    @staticmethod
    @pytest.mark.xfail(raises=NeedChallenge, reason="Challenge is needed, but not implemented yet.")
    async def test_get_starrail_characters(starrail_client: "StarRailBattleChronicleClient"):
        characters = await starrail_client.get_starrail_characters()
        assert len(characters.avatar_list) > 0
        character = characters.avatar_list[-1]
        assert character.id > 0

    @staticmethod
    @pytest.mark.xfail(raises=NeedChallenge, reason="Challenge is needed, but not implemented yet.")
    async def test_get_starrail_challenge(starrail_client: "StarRailBattleChronicleClient"):
        challenge = await starrail_client.get_starrail_challenge()
        assert challenge.season > 0

    @staticmethod
    async def test_get_starrail_rogue(starrail_client: "StarRailBattleChronicleClient"):
        rogue = await starrail_client.get_starrail_rogue()
        assert rogue.role is not None

    @staticmethod
    async def test_get_starrail_museum_info(starrail_client: "StarRailBattleChronicleClient"):
        info = await starrail_client.get_starrail_museum_info()
        assert info is not None

    @staticmethod
    async def test_get_starrail_museum(starrail_client: "StarRailBattleChronicleClient"):
        museum = await starrail_client.get_starrail_museum_detail()
        assert museum is not None
