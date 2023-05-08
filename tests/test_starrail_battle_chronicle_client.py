from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.utils.enum_ import Region

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def starrail_client(starrail_player_id: int, account_id: int, cookies: "Cookies"):
    async with StarRailBattleChronicleClient(
        player_id=starrail_player_id,
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
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
    async def test_get_starrail_notes(starrail_client: "StarRailBattleChronicleClient"):
        notes = await starrail_client.get_starrail_notes()
        assert notes is not None

    @staticmethod
    async def test_get_starrail_characters(
        starrail_client: "StarRailBattleChronicleClient",
    ):
        characters = await starrail_client.get_starrail_characters()
        assert len(characters.avatar_list) > 0
        character = characters.avatar_list[-1]
        assert character.id > 0
