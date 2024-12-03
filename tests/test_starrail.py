from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet.client.starrail import StarRailClient
from simnet.utils.enums import Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def starrail_client(
    starrail_player_id: int,
    region: "Region",
    cookies: "Cookies",
    starrail_cookies: Optional["Cookies"],
):
    if starrail_player_id is None:
        pytest.skip("Test case test_starrail skipped: No starrail player id set.")
    async with StarRailClient(
        player_id=starrail_player_id,
        cookies=starrail_cookies or cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestStarRailClient:
    @staticmethod
    async def test_game(starrail_client: "StarRailClient"):
        assert starrail_client.game == Game.STARRAIL
