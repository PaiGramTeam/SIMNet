from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.calculator.genshin import CalculatorClient
from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enum_ import Region


@pytest_asyncio.fixture
async def calculator_client(genshin_player_id: int, account_id: int, region: "Region", cookies: "Cookies"):
    if genshin_player_id is None:
        pytest.skip("Test case test_starrail_battle_chronicle_client skipped: No starrail player id set.")
    async with CalculatorClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest_asyncio.fixture
async def genshin_battle_chronicle_client(
    genshin_player_id: int, account_id: int, region: "Region", cookies: "Cookies"
):
    async with GenshinBattleChronicleClient(
        player_id=genshin_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestCalculatorClient:
    @staticmethod
    async def test_character_details(
        calculator_client: "CalculatorClient", genshin_battle_chronicle_client: "GenshinBattleChronicleClient"
    ):
        characters = await genshin_battle_chronicle_client.get_genshin_characters()
        character_details = await calculator_client.get_character_details(characters[-1].id)
        assert len(character_details.talents) == 6
        for talent in character_details.talents:
            assert talent.level > -1
        for artifact in character_details.artifacts:
            assert artifact.level >= 0
