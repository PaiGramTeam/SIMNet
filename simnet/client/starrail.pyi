from simnet.client.components.auth import AuthClient
from simnet.client.components.calculator.starrail import StarrailCalculatorClient
from simnet.client.components.chronicle.starrail import StarRailBattleChronicleClient
from simnet.client.components.cloud_game.base import BaseCloudGameClient
from simnet.client.components.daily import DailyRewardClient
from simnet.client.components.diary.starrail import StarrailDiaryClient
from simnet.client.components.lab import LabClient
from simnet.client.components.self_help.starrail import StarrailSelfHelpClient
from simnet.client.components.verify import VerifyClient
from simnet.client.components.wish.starrail import StarRailWishClient
from simnet.utils.enums import Region
from simnet.utils.types import CookieTypes, HeaderTypes, TimeoutTypes

class StarRailClient(
    StarrailCalculatorClient,
    StarRailBattleChronicleClient,
    StarRailWishClient,
    StarrailDiaryClient,
    StarrailSelfHelpClient,
    DailyRewardClient,
    AuthClient,
    LabClient,
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
