"""Starrail Rogue models."""
from typing import List

from simnet.models.base import APIModel

from ..character import RogueCharacter
from .base import PartialTime


class RogueUserRole(APIModel):
    """Rogue User info."""

    nickname: str
    server: str
    level: int


class RogueBasicInfo(APIModel):
    """generalized rogue basic info."""

    unlocked_buff_num: int
    unlocked_miracle_num: int
    unlocked_skill_points: int


class RogueRecordBasic(APIModel):
    """Basic record info."""

    id: int
    finish_cnt: int
    schedule_begin: PartialTime
    schedule_end: PartialTime


class RogueBuffType(APIModel):
    """Rogue buff type."""

    id: int
    name: str
    cnt: int


class RogueBuffItem(APIModel):
    """Rogue buff item."""

    id: int
    name: str
    is_evoluted: bool
    rank: int


class RogueBuff(APIModel):
    """Rogue buff info."""

    base_type: RogueBuffType
    items: List[RogueBuffItem]


class RogueMiracle(APIModel):
    """Rogue miracle info."""

    id: int
    name: str
    icon: str


class RogueRecordDetail(APIModel):
    """Detailed record info."""

    name: str
    finish_time: PartialTime
    score: int
    final_lineup: List[RogueCharacter]
    base_type_list: List[RogueBuffType]
    cached_avatars: List[RogueCharacter]
    buffs: List[RogueBuff]
    miracles: List[RogueMiracle]
    difficulty: int
    progress: int


class RogueRecord(APIModel):
    """generic record data."""

    basic: RogueRecordBasic
    records: List[RogueRecordDetail]
    has_data: bool


class StarRailRogue(APIModel):
    """generic rogue data."""

    role: RogueUserRole
    basic_info: RogueBasicInfo
    current_record: RogueRecord
    last_record: RogueRecord


class RogueLocustBasicCnt(APIModel):
    """Rogue Locust Basic Cnt"""

    narrow: int
    miracle: int
    event: int


class RogueLocustBasicDestiny(APIModel):
    """Rogue Locust Basic Destiny"""

    id: int
    desc: str
    level: int


class RogueLocustBasic(APIModel):
    """Rogue Locust Basic"""

    cnt: RogueLocustBasicCnt
    destiny: List[RogueLocustBasicDestiny]


class RogueLocustRecordDetailBlock(APIModel):
    """Rogue Locust Block"""

    block_id: int
    name: str
    num: int


class RogueLocustRecordDetailFury(APIModel):
    """Rogue Locust Fury"""

    type: int
    point: str


class RogueLocustRecordDetail(APIModel):
    """Detailed Rogue Locust record info."""

    name: str
    finish_time: PartialTime
    final_lineup: List[RogueCharacter]
    base_type_list: List[RogueBuffType]
    cached_avatars: List[RogueCharacter]
    buffs: List[RogueBuff]
    miracles: List[RogueMiracle]
    blocks: List[RogueLocustRecordDetailBlock]
    difficulty: int
    worm_weak: List[str]
    fury: RogueLocustRecordDetailFury

    @property
    def time_str(self) -> str:
        """Get the time as a string."""
        if self.finish_time is None:
            return "N/A"

        return self.finish_time.datetime.strftime("%Y.%m.%d %H:%M")


class RogueLocustRecords(APIModel):
    """Rogue Locust records"""

    records: List[RogueLocustRecordDetail]


class StarRailRogueLocust(APIModel):
    """StarRail Rogue Locust"""

    basic: RogueLocustBasic
    detail: RogueLocustRecords
    role: RogueUserRole
