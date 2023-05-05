from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.client.components.wish.genshin import GenshinWishClient

__all__ = ("GenshinClient",)


class GenshinClient(GenshinBattleChronicleClient, GenshinWishClient, AuthClient):
    """A simple http client for StarRail endpoints."""
