from simnet.client.components.account.auth import AuthClient
from simnet.client.components.chronicle.genshin import GenshinChronicleClient
from simnet.client.components.wish.genshin import WishClient

__all__ = ("GenshinClient",)


class GenshinClient(GenshinChronicleClient, WishClient, AuthClient):
    """A simple http client for StarRail endpoints."""
