from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.components.wish.starrail import StarRailWishClient
from simnet.utils.enum_ import Game

__all__ = ("StarRailClient",)


class StarRailClient(StarRailBattleChronicleClient, StarRailWishClient, AuthClient):
    """A simple http client for StarRail endpoints."""

    game: Optional[Game] = Game.GENSHIN
