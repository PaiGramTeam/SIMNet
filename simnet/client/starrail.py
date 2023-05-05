from simnet.client.components.account.auth import AuthClient
from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.components.wish.starrail import WishClient

__all__ = ("StarRailClient",)


class StarRailClient(StarRailBattleChronicleClient, WishClient, AuthClient):
    """A simple http client for StarRail endpoints."""
