from typing import Optional

from simnet.models.base import APIModel, Field
from simnet.models.starrail.chronicle.base import PartialTime
from simnet.models.zzz.chronicle.challenge import ZZZChallengeBuddy, ZZZChallengeCharacter


class ZZZChallengeMemBos(APIModel):
    """
    Represents a boss in the ZZZ Challenge Memory.

    Attributes:
        icon (str): The icon of the boss.
        name (str): The name of the boss.
        race_icon (str): The race icon of the boss.
        bg_icon (str): The background icon of the boss.
    """

    icon: str
    name: str
    race_icon: str
    bg_icon: str


class ZZZChallengeMemBufferItem(APIModel):
    """
    Represents a buffer item in the ZZZ Challenge Memory.

    Attributes:
        icon (str): The icon of the buffer item.
        desc (str): The description of the buffer item.
        name (str): The name of the buffer item.
    """

    icon: str
    desc: str
    name: str


class ZZZChallengeMemItem(APIModel):
    """
    Represents an item in the ZZZ Challenge Memory.

    Attributes:
        score (int): The score of the challenge.
        star (int): The star rating of the challenge.
        total_star (int): The total star rating.
        challenge_time (PartialTime): The time of the challenge.
        boss (list[ZZZChallengeMemBos]): The list of bosses in the challenge.
        buffer (list[ZZZChallengeMemBufferItem]): The list of buffer items in the challenge.
        avatar_list (list[ZZZChallengeCharacter]): The list of characters in the challenge.
        buddy (Optional[ZZZChallengeBuddy]): The buddy in the challenge, if any.
    """

    score: int
    star: int
    total_star: int
    challenge_time: PartialTime
    boss: list[ZZZChallengeMemBos]
    buffer: list[ZZZChallengeMemBufferItem]
    avatar_list: list[ZZZChallengeCharacter]
    buddy: Optional[ZZZChallengeBuddy] = None


class ZZZChallengeMem(APIModel):
    """
    Represents the memory of a ZZZ Challenge.

    Attributes:
        season (int): The season of the challenge.
        begin_time (Optional[PartialTime]): The start time of the challenge.
        end_time (Optional[PartialTime]): The end time of the challenge.
        rank_percent (int): The rank percentage in the challenge.
        list (list[ZZZChallengeMemItem]): The list of items in the challenge.
        has_data (bool): Indicates if data is available.
        nick_name (str): The nickname of the participant.
        avatar_icon (str): The avatar icon of the participant.
        total_score (int): The total score of the challenge.
        total_star (int): The total star rating of the challenge.
    """

    season: int = Field(alias="zone_id")
    begin_time: Optional[PartialTime] = Field(None, alias="start_time")
    end_time: Optional[PartialTime] = Field(None, alias="end_time")

    rank_percent: int
    list: list[ZZZChallengeMemItem]
    nick_name: str
    avatar_icon: str
    total_score: int
    total_star: int

    has_data: bool
