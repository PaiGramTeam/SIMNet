"""Starrail chronicle challenge."""
from typing import List

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.starrail.character import RogueCharacter

from .base import PartialTime

__all__ = ["StarRailFloor", "FloorNode", "StarRailChallenge"]


class FloorNode(APIModel):
    """Node for a floor."""

    challenge_time: PartialTime
    avatars: List[RogueCharacter]


class StarRailFloor(APIModel):
    """Floor in a challenge."""

    name: str
    round_num: int
    star_num: int
    node_1: FloorNode
    node_2: FloorNode
    is_chaos: bool
    is_fast: bool
    maze_id: int


class StarRailChallenge(APIModel):
    """Challenge in a season."""

    season: int = Field(alias="schedule_id")
    begin_time: PartialTime
    end_time: PartialTime

    total_stars: int = Field(alias="star_num")
    max_floor: str
    total_battles: int = Field(alias="battle_num")
    has_data: bool

    floors: List[StarRailFloor] = Field(alias="all_floor_detail")
