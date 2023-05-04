import datetime
from typing import List, Dict, Any, Literal

from pydantic import Field, root_validator

from simnet.models.base import APIModel
from simnet.models.genshin.character import BaseCharacter

__all__ = (
    "AbyssCharacter",
    "AbyssRankCharacter",
    "Battle",
    "Chamber",
    "CharacterRanks",
    "Floor",
    "SpiralAbyss",
    "SpiralAbyssPair",
)


class AbyssRankCharacter(BaseCharacter):
    """Character with a value of a rank."""

    id: int = Field(alias="avatar_id")
    icon: str = Field(alias="avatar_icon")

    value: int


class AbyssCharacter(BaseCharacter):
    """Character with just a level."""

    level: int


class CharacterRanks(APIModel):
    """Collection of rankings achieved during spiral abyss runs."""

    most_played: List[AbyssRankCharacter] = Field(
        default=[],
        alias="reveal_rank",
    )
    most_kills: List[AbyssRankCharacter] = Field(
        default=[],
        alias="defeat_rank",
    )
    strongest_strike: List[AbyssRankCharacter] = Field(
        default=[],
        alias="damage_rank",
    )
    most_damage_taken: List[AbyssRankCharacter] = Field(
        default=[],
        alias="take_damage_rank",
    )
    most_bursts_used: List[AbyssRankCharacter] = Field(
        default=[],
        alias="energy_skill_rank",
    )
    most_skills_used: List[AbyssRankCharacter] = Field(
        default=[],
        alias="normal_skill_rank",
    )


class Battle(APIModel):
    """Battle in the spiral abyss."""

    half: int = Field(alias="index")
    timestamp: datetime.datetime
    characters: List[AbyssCharacter] = Field(alias="avatars")


class Chamber(APIModel):
    """Chamber of the spiral abyss."""

    chamber: int = Field(alias="index")
    stars: int = Field(alias="star")
    max_stars: Literal[3] = Field(alias="max_star")
    battles: List[Battle]


class Floor(APIModel):
    """Floor of the spiral abyss."""

    floor: int = Field(alias="index")
    # icon: str - unused
    # settle_time: int - appsample might be using this?
    unlocked: Literal[True] = Field(alias="is_unlock")
    stars: int = Field(alias="star")
    max_stars: Literal[9] = Field(alias="max_star")  # maybe one day
    chambers: List[Chamber] = Field(alias="levels")


class SpiralAbyss(APIModel):
    """Information about Spiral Abyss runs during a specific season."""

    unlocked: bool = Field(alias="is_unlock")
    season: int = Field(alias="schedule_id")
    start_time: datetime.datetime
    end_time: datetime.datetime

    total_battles: int = Field(alias="total_battle_times")
    total_wins: str = Field(alias="total_win_times")
    max_floor: str
    total_stars: int = Field(alias="total_star")

    ranks: CharacterRanks

    floors: List[Floor]

    @root_validator(pre=True)
    def nest_ranks(cls, values: Dict[str, Any]) -> Dict[str, AbyssCharacter]:
        """By default, ranks are for some reason on the same level as the rest of the abyss."""
        values.setdefault("ranks", {}).update(values)
        return values


class SpiralAbyssPair(APIModel):
    """Pair of both current and previous spiral abyss.

    This may not be a namedtuple due to how pydantic handles them.
    """

    current: SpiralAbyss
    previous: SpiralAbyss
