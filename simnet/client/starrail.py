from simnet.client.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.wish.starrail import WishClient

__all__ = ("StarRailClient",)


class StarRailClient(StarRailBattleChronicleClient, WishClient):
    """A simple http client for StarRail endpoints."""
