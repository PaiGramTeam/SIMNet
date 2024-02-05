"""Starrail chronicle challenge story."""
from typing import List, Optional

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.starrail.character import RogueCharacter

from .base import PartialTime

__all__ = [
    "StarRailChallengeStoryGroup",
    "StarRailChallengeStoryFloorNode",
    "StarRailChallengeStoryFloor",
    "StarRailChallengeStory",
]


class StarRailChallengeStoryGroup(APIModel):
    """Group in a challenge story."""

    season: int = Field(alias="schedule_id")
    begin_time: PartialTime
    end_time: PartialTime
    status: str
    name_mi18n: str


class StarRailChallengeStoryBuff(APIModel):
    """Challenge Story Buff"""

    id: int
    name_mi18n: str
    desc_mi18n: str
    icon: str


class StarRailChallengeStoryFloorNode(APIModel):
    """Node for a floor."""

    challenge_time: PartialTime
    avatars: List[RogueCharacter]
    buff: Optional[StarRailChallengeStoryBuff] = None
    score: int


class StarRailChallengeStoryFloor(APIModel):
    """Floor in a challenge."""

    name: str
    round_num: int
    star_num: int
    node_1: StarRailChallengeStoryFloorNode
    node_2: StarRailChallengeStoryFloorNode
    is_fast: bool
    maze_id: int

    @property
    def score(self) -> int:
        """Get the score."""
        return self.node_1.score + self.node_2.score


class StarRailChallengeStory(APIModel):
    """Challenge story in a season."""

    groups: List[StarRailChallengeStoryGroup]
    total_stars: int = Field(alias="star_num")
    max_floor: str
    max_floor_id: int
    total_battles: int = Field(alias="battle_num")
    has_data: bool

    floors: List[StarRailChallengeStoryFloor] = Field(alias="all_floor_detail")
