from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.diary.genshin import GenshinDiaryClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def diary_client(genshin_player_id: int, region: "Region", cookies: "Cookies"):
    if genshin_player_id is None:
        pytest.skip(
            "Test case test_genshin_diary_client skipped: No genshin player id set."
        )
    async with GenshinDiaryClient(
        player_id=genshin_player_id,
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestGenshinDiaryClient:
    @staticmethod
    async def test_get_genshin_diary(diary_client: "GenshinDiaryClient"):
        genshin_diary = await diary_client.get_genshin_diary()
        assert genshin_diary is not None
