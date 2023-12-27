from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from simnet.client.components.chronicle.base import BaseChronicleClient

if TYPE_CHECKING:
    from simnet.client.cookies import Cookies
    from simnet.utils.enums import Region


@pytest_asyncio.fixture
async def base_chronicle_client(account_id: int, region: "Region", cookies: "Cookies"):
    async with BaseChronicleClient(
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestBaseChronicleClient:
    @staticmethod
    async def test_get_record_cards(base_chronicle_client: "BaseChronicleClient"):
        record_cards = await base_chronicle_client.get_record_cards()
        assert len(record_cards) > 0
        record_card = record_cards[0]
        assert record_card.uid
