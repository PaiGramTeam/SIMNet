from typing import Optional

from simnet.models.base import APIModel, Field
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
    list: list[ZZZFloorMonsterInfo]


class ZZZFloorNode(APIModel):
    """A node"""

    avatars: list[ZZZChallengeCharacter]
    buddy: Optional[ZZZBaseBuddy] = None
    element_type_list: list[int]
    monster_info: ZZZFloorMonster


class ZZZFloor(APIModel):
    """Floor in a season."""

    layer_index: int
    rating: str
    layer_id: int
    buffs: list[ZZZFloorBuff]
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
    begin_time: Optional[PartialTime] = Field(None, alias="hadal_begin_time")
    end_time: Optional[PartialTime] = Field(None, alias="hadal_end_time")

    fast_layer_time: int
    max_layer: int
    has_data: bool

    rating_list: list[ZZZChallengeRate]
    floors: list[ZZZFloor] = Field(alias="all_floor_detail")

    @property
    def total_stars(self) -> int:
        star_map = {"S": 3, "A": 2, "B": 1}
        return sum(star_map.get(i.rating, 0) * i.times for i in self.rating_list)
