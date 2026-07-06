"""Starrail chronicle challenge."""

from typing import Optional

from simnet.models.base import APIModel, Field
from simnet.models.starrail.character import RogueCharacter

from .base import PartialTime

__all__ = ["StarRailFloor", "FloorNode", "StarRailChallenge"]


class FloorNode(APIModel):
    """Node for a floor."""

    challenge_time: PartialTime
    avatars: list[RogueCharacter]


class StarRailFloor(APIModel):
    """Floor in a challenge."""

    name: str
    round_num: int
    star_num: int
    node_1: FloorNode
    node_2: FloorNode
    node_3: Optional[FloorNode] = None
    is_chaos: bool
    is_fast: bool
    maze_id: int
    extra_star_num: Optional[int] = 0
    is_tierce: Optional[bool] = False


class StarRailChallenge(APIModel):
    """Challenge in a season."""

    season: int = Field(alias="schedule_id")
    begin_time: PartialTime
    end_time: PartialTime

    total_stars: int = Field(alias="star_num")
    max_floor: str
    total_battles: int = Field(alias="battle_num")
    has_data: bool
    extra_star_num: Optional[int] = 0

    floors: list[StarRailFloor] = Field(alias="all_floor_detail")
