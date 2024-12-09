from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.zzz import ZZZBattleChronicleClient
from simnet.client.components.cloud_game.base import BaseCloudGameClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.diary.zzz import ZZZDiaryClient
from simnet.client.components.lab import LabClient
from simnet.client.components.self_help.zzz import ZZZSelfHelpClient
from simnet.client.components.verify import VerifyClient
from simnet.client.components.wish.zzz import ZZZWishClient
from simnet.utils.enums import Game

__all__ = ("ZZZClient",)


class ZZZClient(
    ZZZBattleChronicleClient,
    ZZZWishClient,
    ZZZDiaryClient,
    ZZZSelfHelpClient,
    DailyRewardClient,
    AuthClient,
    LabClient,
    VerifyClient,
    BaseCloudGameClient,
):
    """A simple http client for StarRail endpoints."""

    game: Optional[Game] = Game.ZZZ
