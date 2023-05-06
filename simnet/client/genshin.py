from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.wish.genshin import GenshinWishClient
from simnet.utils.enum_ import Game

__all__ = ("GenshinClient",)


class GenshinClient(GenshinBattleChronicleClient, GenshinWishClient, AuthClient, DailyRewardClient):
    """A simple http client for StarRail endpoints."""

    game: Optional[Game] = Game.GENSHIN
