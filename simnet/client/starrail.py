from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.components.wish.starrail import StarRailWishClient

__all__ = ("StarRailClient",)


class StarRailClient(StarRailBattleChronicleClient, StarRailWishClient, AuthClient):
    """A simple http client for StarRail endpoints."""
