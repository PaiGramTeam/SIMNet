from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from simnet.client.components.calculator.starrail import StarrailCalculatorClient
from simnet.utils.enums import Game

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def calculator_client(
    starrail_player_id: int, region: "Region", cookies: "Cookies", starrail_cookies: Optional["Cookies"]
):
    if starrail_player_id is None:
        pytest.skip("Test case test_starrail_calculator_client skipped: No starrail player id set.")
    async with StarrailCalculatorClient(
        player_id=starrail_player_id,
        cookies=starrail_cookies or cookies,
        region=region,
        lang="zh-cn",
    ) as client_instance:
        client_instance.game = Game.STARRAIL
        yield client_instance


@pytest.mark.asyncio
class TestCalculatorClient:
    @staticmethod
    async def test_character_details(calculator_client: "StarrailCalculatorClient"):
        characters = await calculator_client.get_calculator_characters()
        character_details = await calculator_client.get_character_details(characters[-1].id)
        assert len(character_details.skills) == 4
        for talent in character_details.skills:
            assert talent.cur_level > -1
