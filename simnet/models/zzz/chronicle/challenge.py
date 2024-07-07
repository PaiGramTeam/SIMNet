from typing import List, Optional

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.starrail.chronicle.base import PartialTime
from simnet.models.zzz.character import ZZZBaseBuddy, ZZZBaseCharacter


class ZZZFloorBuff(APIModel):
    """A buff"""

    title: str
    text: str


class ZZZChallengeCharacter(ZZZBaseCharacter):
    """Challenge character"""

    level: int


class ZZZFloorMonsterInfo(APIModel):
    """Monster info"""

    id: int
    name: str
    weak_element_type: int


class ZZZFloorMonster(APIModel):
    """Monster"""

    level: int
    list: List[ZZZFloorMonsterInfo]


class ZZZFloorNode(APIModel):
    """A node"""

    avatars: List[ZZZChallengeCharacter]
    buddy: ZZZBaseBuddy
    element_type_list: List[int]
    monster_info: ZZZFloorMonster


class ZZZFloor(APIModel):
    """Floor in a season."""

    layer_index: int
    rating: str
    layer_id: int
    buffs: List[ZZZFloorBuff]
    node_1: ZZZFloorNode
    node_2: ZZZFloorNode
    challenge_time: str
    zone_name: str
    floor_challenge_time: PartialTime


class ZZZChallengeRate(APIModel):
    """A challenge rate."""

    times: int
    rating: str


class ZZZChallenge(APIModel):
    """Challenge in a season."""

    season: int = Field(alias="schedule_id")
    begin_time: Optional[PartialTime] = Field(alias="hadal_begin_time")
    end_time: Optional[PartialTime] = Field(alias="hadal_end_time")

    fast_layer_time: int
    max_layer: int
    has_data: bool

    rating_list: List[ZZZChallengeRate]
    floors: List[ZZZFloor] = Field(alias="all_floor_detail")
