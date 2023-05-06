import os
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from simnet.client.starrail import StarRailClient

player_id = int(os.environ.get("STARRAIL_PLAYER_ID"))


@pytest.mark.asyncio
class TestStarRailClient:
    @staticmethod
    async def test_get_starrail_record(starrail_client: "StarRailClient"):
        global player_id
        record = await starrail_client.get_record_card()
        assert record is not None
        assert player_id == record.uid

    @staticmethod
    async def test_get_starrail_user(starrail_client: "StarRailClient"):
        user = await starrail_client.get_starrail_user(player_id=player_id)
        assert user is not None
        assert user.stats.chest_num > 0
        assert len(user.characters) > 0
        character = user.characters[-1]
        assert character.id > 0

    @staticmethod
    async def test_get_starrail_notes(starrail_client: "StarRailClient"):
        notes = await starrail_client.get_starrail_notes(player_id=player_id)
        assert notes is not None

    @staticmethod
    async def test_get_starrail_characters(starrail_client: "StarRailClient"):
        characters = await starrail_client.get_starrail_characters(player_id=player_id)
        assert len(characters.avatar_list) > 0
        character = characters.avatar_list[-1]
        assert character.id > 0
