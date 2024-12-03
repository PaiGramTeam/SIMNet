from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet.client.zzz import ZZZClient
from simnet.utils.enums import Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def zzz_client(zzz_player_id: int, region: "Region", cookies: "Cookies", zzz_cookies: Optional["Cookies"]):
    if zzz_player_id is None:
        pytest.skip("Test case test_zzz skipped: No zzz player id set.")
    async with ZZZClient(
        player_id=zzz_player_id,
        cookies=zzz_cookies or cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestZZZClient:
    @staticmethod
    async def test_game(zzz_client: "ZZZClient"):
        assert zzz_client.game == Game.ZZZ
