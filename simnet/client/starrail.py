from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.calculator.starrail import StarrailCalculatorClient
from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.components.cloud_game.base import BaseCloudGameClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.diary.starrail import StarrailDiaryClient
from simnet.client.components.lab import LabClient
from simnet.client.components.self_help.starrail import StarrailSelfHelpClient
from simnet.client.components.verify import VerifyClient
from simnet.client.components.wish.starrail import StarRailWishClient
from simnet.utils.enums import Game

__all__ = ("StarRailClient",)


class StarRailClient(
    StarrailCalculatorClient,
    StarRailBattleChronicleClient,
    StarRailWishClient,
    StarrailDiaryClient,
    StarrailSelfHelpClient,
    DailyRewardClient,
    AuthClient,
    LabClient,
    VerifyClient,
    BaseCloudGameClient,
):
    """A simple http client for StarRail endpoints."""

    game: Optional[Game] = Game.STARRAIL
