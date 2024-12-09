from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet import StarRailClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def starrail_client(
    starrail_player_id: int, region: "Region", cookies: "Cookies", starrail_cookies: Optional["Cookies"]
):
    if starrail_player_id is None:
        pytest.skip("Test case test_starrail_cloud_game_client skipped: No starrail player id set.")
    async with StarRailClient(
        player_id=starrail_player_id,
        cookies=starrail_cookies or cookies,
        region=region,
        lang="zh-cn",
    ) as client_instance:
        if not client_instance.cloud_game_combo_token:
            pytest.skip("Test case test_starrail_cloud_game_client skipped: No cloud game token set.")
        yield client_instance


@pytest.mark.asyncio
class TestStarrailCloudGameClient:
    @staticmethod
    async def test_check_cloud_game_token(starrail_client: StarRailClient):
        data = await starrail_client.check_cloud_game_token()
        assert data

    @staticmethod
    async def test_get_cloud_game_wallet(starrail_client: StarRailClient):
        data = await starrail_client.get_cloud_game_wallet()
        assert data

    @staticmethod
    async def test_get_cloud_game_notifications(starrail_client: StarRailClient):
        data = await starrail_client.get_cloud_game_notifications()
        assert "list" in data
