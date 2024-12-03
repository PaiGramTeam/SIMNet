"""Starrail chronicle stats."""

from collections.abc import Sequence

from simnet.models.base import APIModel, Field

from .. import character

__all__ = [
    "PartialStarRailUserStats",
    "StarRailUserInfo",
    "StarRailUserStats",
    "StarRailStats",
]


class StarRailStats(APIModel):
    """Overall user stats."""

    active_days: int
    avatar_num: int
    achievement_num: int
    chest_num: int
    abyss_process: str
    dream_paster_num: int


class PartialStarRailUserStats(APIModel):
    """User stats with characters without equipment."""

    stats: StarRailStats
    characters: Sequence[character.StarRailPartialCharacter] = Field(alias="avatar_list")


class StarRailUserInfo(APIModel):
    """User info."""

    nickname: str
    server: str = Field(alias="region")
    level: int
    avatar: str


class StarRailUserStats(PartialStarRailUserStats):
    """User stats."""

    info: StarRailUserInfo
    cur_head_icon_url: str
    phone_background_image_url: str
