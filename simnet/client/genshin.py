from simnet.client.account.auth import AuthClient
from simnet.client.chronicle.genshin import GenshinChronicleClient
from simnet.client.wish.genshin import WishClient

__all__ = ("GenshinClient",)


class GenshinClient(GenshinChronicleClient, WishClient, AuthClient):
    """A simple http client for StarRail endpoints."""
