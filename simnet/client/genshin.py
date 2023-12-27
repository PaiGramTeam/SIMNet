from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.calculator.genshin import CalculatorClient
from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.diary.genshin import GenshinDiaryClient
from simnet.client.components.lab import LabClient
from simnet.client.components.transaction import TransactionClient
from simnet.client.components.verify import VerifyClient
from simnet.client.components.wish.genshin import GenshinWishClient
from simnet.utils.enums import Game

__all__ = ("GenshinClient",)


class GenshinClient(
    CalculatorClient,
    GenshinBattleChronicleClient,
    GenshinWishClient,
    GenshinDiaryClient,
    AuthClient,
    DailyRewardClient,
    LabClient,
    TransactionClient,
    VerifyClient,
):
    """A simple http client for Genshin endpoints."""

    game: Optional[Game] = Game.GENSHIN
