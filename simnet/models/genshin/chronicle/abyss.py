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
    """A character in Spiral Abyss with a rank.

    Attributes:
        id (int): The ID of the character.
        icon (str): The icon of the character.
        value (int): The rank of the character.
    """

    id: int = Field(alias="avatar_id")
    icon: str = Field(alias="avatar_icon")
    value: int


class AbyssCharacter(BaseCharacter):
    """A character in Spiral Abyss with just a level.

    Attributes:
        level (int): The level of the character.
    """

    level: int


class CharacterRanks(APIModel):
    """A collection of character rankings achieved during Spiral Abyss runs.

    Attributes:
        most_played (List[AbyssRankCharacter]): The characters played the most.
        most_kills (List[AbyssRankCharacter]): The characters that have killed the most enemies.
        strongest_strike (List[AbyssRankCharacter]): The characters that have dealt the most damage in a single hit.
        most_damage_taken (List[AbyssRankCharacter]): The characters that have taken the most damage.
        most_bursts_used (List[AbyssRankCharacter]): The characters that have used their elemental burst skill the most.
        most_skills_used (List[AbyssRankCharacter]): The characters that have used their elemental skill the most.
    """

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
    """A battle in Spiral Abyss.

    Attributes:
        half (int): The half (1 or 2) of the chamber in which the battle took place.
        timestamp (datetime.datetime): The timestamp when the battle took place.
        characters (List[AbyssCharacter]): The characters that participated in the battle.
    """

    half: int = Field(alias="index")
    timestamp: datetime.datetime
    characters: List[AbyssCharacter] = Field(alias="avatars")


class Chamber(APIModel):
    """A chamber in Spiral Abyss.

    Attributes:
        chamber (int): The index of the chamber.
        stars (int): The number of stars obtained in the chamber.
        max_stars (Literal[3]): The maximum number of stars that can be obtained in the chamber (currently always 3).
        battles (List[Battle]): The battles that took place in the chamber.
    """

    chamber: int = Field(alias="index")  # skipcq: PTC-W0052
    stars: int = Field(alias="star")
    max_stars: Literal[3] = Field(alias="max_star")
    battles: List[Battle]


class Floor(APIModel):
    """A floor in Spiral Abyss.

    Attributes:
        floor (int): The index of the floor.
        unlocked (Literal[True]): Whether the floor is unlocked (always True).
        stars (int): The total number of stars obtained in the floor.
        max_stars (Literal[9]): The maximum number of stars that can be obtained in the floor (currently always 9).
        chambers (List[Chamber]): The chambers that make up the floor.
    """

    floor: int = Field(alias="index")  # skipcq: PTC-W0052
    unlocked: Literal[True] = Field(alias="is_unlock")
    stars: int = Field(alias="star")
    max_stars: Literal[9] = Field(alias="max_star")  # maybe one day
    chambers: List[Chamber] = Field(alias="levels")


class SpiralAbyss(APIModel):
    """Information about Spiral Abyss runs during a specific season.

    Attributes:
        unlocked (bool): Whether the Spiral Abyss is unlocked.
        season (int): The ID of the season.
        start_time (datetime.datetime): The start time of the season.
        end_time (datetime.datetime): The end time of the season.
        total_battles (int): The total number of battles fought during the season.
        total_wins (str): The total number of battles won during the season.
        max_floor (str): The highest floor reached during the season.
        total_stars (int): The total number of stars obtained during the season.
        ranks (CharacterRanks): The rankings achieved during the season.
        floors (List[Floor]): The floors of the Spiral Abyss during the season.
    """

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
    """A pair of both current and previous Spiral Abyss information.

    Attributes:
        current (SpiralAbyss): The current Spiral Abyss information.
        previous (SpiralAbyss): The previous Spiral Abyss information.
    """

    current: SpiralAbyss
    previous: SpiralAbyss
