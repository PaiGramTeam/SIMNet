from datetime import datetime
from enum import StrEnum

from simnet.models.base import APIModel


class StarRailSelfHelpActionLogReason(StrEnum):
    """
    Possible reasons for a StarRail self-help action log.

    Attributes:
        LOG_OUT: Log out.
        LOG_IN: Log in.
    """

    LOG_OUT = "登出"
    LOG_IN = "登入"


class StarRailSelfHelpActionLog(APIModel):
    """
    StarRail self-help action log.

    Attributes:
        id: The log ID.
        uid: The user ID.
        time: The time of the log.
        reason: The reason for the log.
        client_ip: The client IP address.
    """

    id: int
    uid: int
    time: datetime
    reason: StarRailSelfHelpActionLogReason
    client_ip: str | None = ""

    @property
    def status(self) -> int:
        return 1 if self.reason == StarRailSelfHelpActionLogReason.LOG_IN else 0
