from datetime import datetime
from typing import List

from simnet.models.base import APIModel


class RewardHistoryAwardItem(APIModel):
    """Reward history award item."""

    name: str
    num: int
    pic: str
    pic_bg: str
    sort: int
    is_main: bool


class RewardHistoryItem(APIModel):
    """Reward history item."""

    award: List[RewardHistoryAwardItem]
    pack_name: str
    ts: datetime
    task_name: str


class RewardHistory(APIModel):
    """Reward history."""

    list: List[RewardHistoryItem]
    count: int
    time: str
