"""Starrail chronicle stats."""

import typing

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.zzz import character


class ZZZStats(APIModel):
    """Overall user stats."""

    active_days: int
    avatar_num: int
    world_level_name: str
    cur_period_zone_layer_count: int
    buddy_num: int


class ZZZAvatarBasic(APIModel):
    """Basic avatar"""

    characters: typing.Sequence[character.ZZZPartialCharacter] = Field(alias="avatar_list")


class ZZZBuddyBasic(APIModel):
    """Basic buddy"""

    buddy_list: typing.Sequence[character.ZZZPartialBuddy] = Field(alias="list")


class ZZZUserStats(ZZZAvatarBasic):
    """User stats with characters without equipment."""

    stats: ZZZStats
    cur_head_icon_url: str
    buddy_list: typing.Sequence[character.ZZZPartialBuddy]
