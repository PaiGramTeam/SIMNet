from typing import Optional

from simnet.client.components.auth import AuthClient
from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.diary.genshin import GenshinDiaryClient
from simnet.client.components.lab import LabClient
from simnet.client.components.wish.genshin import GenshinWishClient
from simnet.utils.enum_ import Region
from simnet.utils.types import CookieTypes, HeaderTypes, TimeoutTypes


class GenshinClient(
    GenshinBattleChronicleClient, GenshinWishClient, GenshinDiaryClient, AuthClient, DailyRewardClient, LabClient
):
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
