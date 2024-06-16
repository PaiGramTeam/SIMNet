from datetime import datetime
from typing import Optional

from simnet.models.base import APIModel


class StarRailSelfHelpActionLog(APIModel):
    """StarRail self-help action log."""

    id: int
    uid: int
    time: datetime
    reason: str
    client_ip: Optional[str] = ""

    @property
    def status(self) -> int:
        return 1 if self.reason == "登入" else 0
