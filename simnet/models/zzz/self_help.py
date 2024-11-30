from datetime import datetime
from enum import Enum
from typing import Optional

from simnet.models.base import APIModel, Field


class ZZZSelfHelpActionLogReason(str, Enum):
    """
    Possible reasons for a ZZZ self-help action log.

    Attributes:
        LOG_OUT: Log out.
        LOG_IN: Log in.
    """

    LOG_OUT = "登出"
    LOG_IN = "登录"


class ZZZSelfHelpActionLog(APIModel):
    """
    ZZZ self-help action log.

    Attributes:
        id: The log ID.
        uid: The user ID.
        time: The time of the log.
        reason: The reason for the log.
        client_ip: The client IP address.
    """

    id: int
    uid: int
    time: datetime = Field(alias="datetime")
    reason: ZZZSelfHelpActionLogReason = Field(alias="action_name")
    client_ip: Optional[str] = ""

    @property
    def status(self) -> int:
        return 1 if self.reason == ZZZSelfHelpActionLogReason.LOG_IN else 0
