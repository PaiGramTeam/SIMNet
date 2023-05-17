from typing import List
from pydantic import Field
from simnet.models.base import APIModel
from simnet.models.starrail.chronicle.characters import PartialCharacter


class Stats(APIModel):
    """
    Statistics of user data.

    Attributes:
        active_days (int): Number of days the user has been active.
        avatar_num (int): Number of avatars the user has.
        achievement_num (int): Number of achievements the user has earned.
        chest_num  (int): Number of chests the user has opened.
        abyss_process (str): Progress of the user in the abyss mode.
    """

    active_days: int
    avatar_num: int
    achievement_num: int
    chest_num: int
    abyss_process: str


class PartialStarRailUserStats(APIModel):
    """
    Partial data of StarRail user, containing statistics and character information.

    Attributes:
        stats (Stats): Statistics of user data.
        characters (List[PartialCharacter]): List of user's avatars/characters.
    """

    stats: Stats
    characters: List[PartialCharacter] = Field(alias="avatar_list")


class StarRailUserInfo(APIModel):
    """
    Information of StarRail user.

    Attributes:
        nickname (str): User's nickname.
        server (str): User's server.
        level (int): User's level.
        avatar (str): User's avatar url.
    """

    nickname: str
    server: str = Field(alias="region")
    level: int
    avatar: str


class StarRailUserStats(PartialStarRailUserStats):
    """Complete data of StarRail user, containing statistics and character information."""

    info: StarRailUserInfo
