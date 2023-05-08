from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.lab import LabClient
from simnet.client.components.wish.starrail import StarRailWishClient
from simnet.utils.enum_ import Region
from simnet.utils.types import CookieTypes, HeaderTypes, TimeoutTypes


class StarRailClient(StarRailBattleChronicleClient, StarRailWishClient,DailyRewardClient, AuthClient, LabClient):
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
