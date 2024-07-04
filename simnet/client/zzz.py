from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.lab import LabClient
from simnet.client.components.verify import VerifyClient
from simnet.client.components.wish.zzz import ZZZWishClient
from simnet.utils.enums import Game

__all__ = ("ZZZClient",)


class ZZZClient(
    ZZZWishClient,
    DailyRewardClient,
    AuthClient,
    LabClient,
    VerifyClient,
):
    """A simple http client for StarRail endpoints."""

    game: Optional[Game] = Game.ZZZ
