from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet import GenshinClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def genshin_client(genshin_player_id: int, region: "Region", cookies: "Cookies"):
    if genshin_player_id is None:
        pytest.skip("Test case test_genshin_cloud_game_client skipped: No genshin player id set.")
    async with GenshinClient(
        player_id=genshin_player_id,
        cookies=cookies,
        region=region,
    ) as client_instance:
        if not client_instance.cloud_game_combo_token:
            pytest.skip("Test case test_genshin_cloud_game_client skipped: No cloud game token set.")
        yield client_instance


@pytest.mark.asyncio
class TestGenshinCloudGameClient:
    @staticmethod
    async def test_check_cloud_game_token(genshin_client: GenshinClient):
        data = await genshin_client.check_cloud_game_token()
        assert data

    @staticmethod
    async def test_get_cloud_game_wallet(genshin_client: GenshinClient):
        data = await genshin_client.get_cloud_game_wallet()
        assert data

    @staticmethod
    async def test_get_cloud_game_notifications(genshin_client: GenshinClient):
        data = await genshin_client.get_cloud_game_notifications()
        assert "list" in data
