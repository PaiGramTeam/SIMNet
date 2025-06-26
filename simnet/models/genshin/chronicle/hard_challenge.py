import enum
from typing import Optional

from simnet.models.base import APIModel, DateTimeField, Field
from simnet.models.genshin.character import BaseCharacter
from simnet.models.starrail.chronicle.base import PartialTime


class HardChallengeSchedule(APIModel):
    """Hard challenge schedule."""

    start_time: DateTimeField
    end_time: DateTimeField
    id: int = Field(alias="schedule_id")
    start_date_time: Optional[PartialTime] = None
    end_date_time: Optional[PartialTime] = None

    is_valid: bool
    name: str


class HardChallengeDifficulty(enum.IntEnum):
    """The difficulty of the imaginarium theater data."""

    NULL = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    VICIOUS = 4
    FEARLESS = 5
    DEAD_HARD = 6
    HARD_PLUS = 7


class HardChallengeSingleBestData(APIModel):
    """
    Represents the best performance data for a single challenge in a hard challenge.

    Attributes:
        difficulty (int): The difficulty level of the challenge.
        second (int): The duration of the challenge in seconds.
        icon (str): The URL or path to the icon representing the challenge.
    """

    difficulty: HardChallengeDifficulty
    second: int
    icon: str


class HardChallengeSingleChallengeAvatar(BaseCharacter):
    """
    Represents the avatar data for a single challenge in a hard challenge.

    Attributes:
        id (int): The unique identifier for the avatar, aliased as 'avatar_id'.
        icon (str): The URL or path to the image of the avatar, aliased as 'image'.
        level (int): The level of the avatar.
        rank (int): The rank of the avatar.
    """

    id: int = Field(alias="avatar_id")
    icon: str = Field(alias="image")
    level: int
    rank: int


class HardChallengeSingleChallengeBestAvatar(BaseCharacter):
    """
    Represents the best-performing avatar data for a single challenge in a hard challenge.

    Attributes:
        id (int): The unique identifier for the avatar, aliased as 'avatar_id'.
        icon (str): The URL or path to the side icon image of the avatar.
        dps (int): The damage per second (DPS) value of the avatar.
        type (int): The type or category of the avatar.
    """

    id: int = Field(alias="avatar_id")
    icon: str = Field(alias="side_icon")
    dps: int
    type: int


class HardChallengeSingleChallengeBoss(BaseCharacter):
    """
    Represents the boss data for a single challenge in a hard challenge.

    Attributes:
        id (int): The unique identifier for the boss, aliased as 'monster_id'.
        level (int): The level of the boss.
        desc (list[str]): A list of descriptions for the boss.
    """

    id: int = Field(alias="monster_id")
    level: int
    desc: list[str]


class HardChallengeSingleChallengeData(APIModel):
    """
    Represents the data structure for a single challenge in a hard challenge.

    Attributes:
        name (str): The name of the challenge.
        second (int): The duration of the challenge in seconds.
        teams (list[HardChallengeSingleChallengeAvatar]): A list of avatars participating in the challenge.
        best_avatar (list[HardChallengeSingleChallengeBestAvatar]): A list of the best-performing avatars in the challenge.
        monster (HardChallengeSingleChallengeBoss): The boss associated with the challenge.
    """

    name: str
    second: int
    teams: list[HardChallengeSingleChallengeAvatar]
    best_avatar: list[HardChallengeSingleChallengeBestAvatar]
    monster: HardChallengeSingleChallengeBoss


class HardChallengeSingleData(APIModel):
    """
    Represents the single challenge data for a hard challenge.

    Attributes:
        best (Optional[HardChallengeSingleBestData]): The best performance data for the single challenge.
        challenge (list): A list of challenges associated with the hard challenge.
        has_data (bool): Indicates whether the single challenge contains valid data.
    """

    best: Optional[HardChallengeSingleBestData] = None
    challenge: list[HardChallengeSingleChallengeData]
    has_data: bool


class HardChallengeData(APIModel):
    """
    Represents the data structure for a hard challenge.

    Attributes:
        schedule (HardChallengeSchedule): The schedule information for the hard challenge.
        single (HardChallengeSingleData): The single challenge data, including the best performance and challenge details.
    """

    schedule: HardChallengeSchedule
    single: HardChallengeSingleData


class GenshinHardChallenge(APIModel):
    """Hard Challenge."""

    data: list[HardChallengeData]
    unlocked: bool = Field(alias="is_unlock")
