from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet.client.components.diary.zzz import ZZZDiaryClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def diary_client(zzz_player_id: int, region: "Region", cookies: "Cookies", zzz_cookies: Optional["Cookies"]):
    if zzz_player_id is None:
        pytest.skip("Test case test_zzz skipped: No zzz player id set.")
    async with ZZZDiaryClient(
        player_id=zzz_player_id,
        cookies=zzz_cookies or cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestZZZDiaryClient:
    @staticmethod
    async def test_get_zzz_diary(diary_client: "ZZZDiaryClient"):
        genshin_diary = await diary_client.get_zzz_diary()
        assert genshin_diary is not None
