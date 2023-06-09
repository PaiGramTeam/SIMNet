from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.diary.starrail import StarrailDiaryClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enum_ import Region


@pytest_asyncio.fixture
async def diary_client(starrail_player_id: int, account_id: int, region: "Region", cookies: "Cookies"):
    if starrail_player_id is None:
        pytest.skip("Test case test_starrail_diary_client skipped: No starrail player id set.")
    async with StarrailDiaryClient(
        player_id=starrail_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestStarrailDiaryClient:
    @staticmethod
    async def test_get_starrail_diary(diary_client: "StarrailDiaryClient"):
        genshin_diary = await diary_client.get_starrail_diary()
        assert genshin_diary is not None
