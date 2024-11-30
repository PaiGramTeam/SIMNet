"""Starrail chronicle challenge story."""

from typing import List, Optional

from simnet.models.base import APIModel, Field
from simnet.models.starrail.character import RogueCharacter

from .base import PartialTime

__all__ = [
    "StarRailChallengeBossBoss",
    "StarRailChallengeBossGroup",
    "StarRailChallengeBossBuff",
    "StarRailChallengeBossFloorNode",
    "StarRailChallengeBossFloor",
    "StarRailChallengeBoss",
]


class StarRailChallengeBossBoss(APIModel):
    """Boss in a challenge boss."""

    id: int
    name_mi18n: str
    icon: str


class StarRailChallengeBossGroup(APIModel):
    """Group in a challenge boss."""

    season: int = Field(alias="schedule_id")
    begin_time: PartialTime
    end_time: PartialTime
    status: str
    name_mi18n: str
    upper_boss: StarRailChallengeBossBoss
    lower_boss: StarRailChallengeBossBoss


class StarRailChallengeBossBuff(APIModel):
    """Challenge boss Buff"""

    id: int
    name_mi18n: str
    desc_mi18n: str
    icon: str


class StarRailChallengeBossFloorNode(APIModel):
    """Node for a floor."""

    challenge_time: Optional[PartialTime] = None
    avatars: List[RogueCharacter]
    buff: Optional[StarRailChallengeBossBuff] = None
    score: int
    boss_defeated: bool

    @property
    def has_data(self) -> bool:
        """Check if the node has data."""
        return bool(self.avatars)


class StarRailChallengeBossFloor(APIModel):
    """Floor in a challenge."""

    name: str
    star_num: int
    node_1: StarRailChallengeBossFloorNode
    node_2: StarRailChallengeBossFloorNode
    is_fast: bool
    maze_id: int
    last_update_time: PartialTime

    @property
    def score(self) -> int:
        """Get the score."""
        return self.node_1.score + self.node_2.score


class StarRailChallengeBoss(APIModel):
    """Challenge boss in a season."""

    groups: List[StarRailChallengeBossGroup]
    total_stars: int = Field(alias="star_num")
    max_floor: str
    max_floor_id: int
    total_battles: int = Field(alias="battle_num")
    has_data: bool

    floors: List[StarRailChallengeBossFloor] = Field(alias="all_floor_detail")
