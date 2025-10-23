from simnet.client.components.auth import AuthClient
from simnet.client.components.calculator.genshin import CalculatorClient
from simnet.client.components.chronicle.genshin import GenshinBattleChronicleClient
from simnet.client.components.cloud_game.base import BaseCloudGameClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.diary.genshin import GenshinDiaryClient
from simnet.client.components.lab import LabClient
from simnet.client.components.transaction import TransactionClient
from simnet.client.components.verify import VerifyClient
from simnet.client.components.wish.genshin import (
    GenshinBeyondWishClient,
    GenshinWishClient,
)
from simnet.utils.enums import Region
from simnet.utils.types import CookieTypes, HeaderTypes, TimeoutTypes

class GenshinClient(
    CalculatorClient,
    GenshinBattleChronicleClient,
    GenshinWishClient,
    GenshinBeyondWishClient,
    GenshinDiaryClient,
    AuthClient,
    DailyRewardClient,
    LabClient,
    TransactionClient,
    VerifyClient,
    BaseCloudGameClient,
):
    def __init__(
        self,
        cookies: CookieTypes | None = None,
        headers: HeaderTypes | None = None,
        account_id: int | None = None,
        player_id: int | None = None,
        region: Region = ...,
        lang: str = "en-us",
        timeout: TimeoutTypes | None = None,
        device_id: str | None = None,
        device_fp: str | None = None,
    ): ...
