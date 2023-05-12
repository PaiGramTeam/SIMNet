from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.genshin import GenshinClient
from simnet.utils.enum_ import Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enum_ import Region


@pytest_asyncio.fixture
async def genshin_client(genshin_player_id: int, account_id: int, region: "Region", cookies: "Cookies"):
    async with GenshinClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinClient:
    @staticmethod
    async def test_game(genshin_client: "GenshinClient"):
        assert genshin_client.game == Game.GENSHIN
