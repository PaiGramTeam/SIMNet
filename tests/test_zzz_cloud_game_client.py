from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet import ZZZClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def zzz_client(zzz_player_id: int, region: "Region", cookies: "Cookies", zzz_cookies: Optional["Cookies"]):
    if zzz_player_id is None:
        pytest.skip("Test case test_zzz_cloud_game_client skipped: No genshin player id set.")
    async with ZZZClient(
        player_id=zzz_player_id,
        cookies=zzz_cookies or cookies,
        region=region,
    ) as client_instance:
        if not client_instance.cloud_game_combo_token:
            pytest.skip("Test case test_zzz_cloud_game_client skipped: No cloud game token set.")
        yield client_instance


@pytest.mark.asyncio
class TestZZZCloudGameClient:
    @staticmethod
    async def test_check_cloud_game_token(zzz_client: ZZZClient):
        data = await zzz_client.check_cloud_game_token()
        assert data

    @staticmethod
    async def test_get_cloud_game_wallet(zzz_client: ZZZClient):
        data = await zzz_client.get_cloud_game_wallet()
        assert data

    @staticmethod
    async def test_get_cloud_game_notifications(zzz_client: ZZZClient):
        data = await zzz_client.get_cloud_game_notifications()
        assert "list" in data
