from typing import Optional

from simnet.client.account.auth import AuthClient
from simnet.client.chronicle.genshin import GenshinChronicleClient
from simnet.client.wish.genshin import WishClient
from simnet.utils.enum_ import Region
from simnet.utils.types import CookieTypes, HeaderTypes, TimeoutTypes

class GenshinClient(GenshinChronicleClient, WishClient, AuthClient):
    def __init__(
        self,
        cookies: Optional[CookieTypes] = None,
        headers: Optional[HeaderTypes] = None,
        account_id: Optional[int] = None,
        player_id: Optional[int] = None,
        region: Region = Region.OVERSEAS,
        lang: str = "en-us",
        timeout: Optional[TimeoutTypes] = None,
    ): ...
