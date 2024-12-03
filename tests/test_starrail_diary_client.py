from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet.client.components.diary.starrail import StarrailDiaryClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def diary_client(
    starrail_player_id: int,
    region: "Region",
    cookies: "Cookies",
    starrail_cookies: Optional["Cookies"],
):
    if starrail_player_id is None:
        pytest.skip(
            "Test case test_starrail_diary_client skipped: No starrail player id set."
        )
    async with StarrailDiaryClient(
        player_id=starrail_player_id,
        cookies=starrail_cookies or cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestStarrailDiaryClient:
    @staticmethod
    async def test_get_starrail_diary(diary_client: "StarrailDiaryClient"):
        genshin_diary = await diary_client.get_starrail_diary()
        assert genshin_diary is not None
