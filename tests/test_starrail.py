from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.starrail import StarRailClient
from simnet.utils.enum_ import Region, Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def starrail_client(
    starrail_player_id: int, account_id: int, cookies: "Cookies"
):  # skipcq: PY-D0003  # skipcq: PYL-W0621
    async with StarRailClient(
        player_id=starrail_player_id,
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestStarRailClient:
    @staticmethod
    async def test_game(starrail_client: "StarRailClient"):
        assert starrail_client.game == Game.STARRAIL
