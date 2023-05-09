from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.calculator.genshin import CalculatorClient
from simnet.utils.enum_ import Region

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies


@pytest_asyncio.fixture
async def calculator_client(
    genshin_player_id: int, account_id: int, cookies: "Cookies"
):
    async with CalculatorClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=Region.CHINESE,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestCalculatorClient:
    @staticmethod
    async def test_get_battle_chronicle(calculator_client: "CalculatorClient"):
        character_details = await calculator_client.get_character_details(10000046)
        assert len(character_details.talents) == 6
        for talent in character_details.talents:
            assert talent.level == 10 or talent.max_level == 13 or talent.max_level == 1
        for artifact in character_details.artifacts:
            assert artifact.level >= 0
