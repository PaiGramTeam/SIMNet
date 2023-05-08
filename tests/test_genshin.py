from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.genshin import GenshinClient
from simnet.utils.enum_ import Region, Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def genshin_client(
    genshin_player_id: int, account_id: int, cookies: "Cookies"
):  # skipcq: PY-D0003  # skipcq: PYL-W0621
    async with GenshinClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinClient:
    async def test_game(self, genshin_client: "GenshinClient"):
        assert genshin_client.game == Game.GENSHIN
