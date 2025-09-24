from enum import Enum
from typing import Optional

from simnet.models.base import APIModel, Field

from ..character import RogueCharacter
from .base import PartialTime


class StarRailChallengePeakGroup(APIModel):
    """
    Represents a challenge peak group in Star Rail.

    Attributes:
        season (int): The season number, aliased as "group_id".
        begin_time (PartialTime): The start time of the challenge.
        end_time (PartialTime): The end time of the challenge.
        status (str): The current status of the group.
        name_mi18n (str): The multilingual name of the group.
        game_version (str): The game version.
        theme_pic_path (str): The path to the theme image.
    """

    season: int = Field(alias="group_id")
    begin_time: PartialTime
    end_time: PartialTime
    status: str
    name_mi18n: str

    game_version: str
    theme_pic_path: str


class StarRailChallengePeakBossInfo(APIModel):
    """
    Represents information about a boss in the Star Rail Challenge Peak.

    Attributes:
        maze_id (int): The unique identifier for the maze.
        name (str): The multilingual name of the boss, aliased as "name_mi18n".
        hard_mode_name (str): The multilingual name of the boss in hard mode, aliased as "hard_mode_name_mi18n".
        icon (str): The icon representing the boss.
    """

    maze_id: int
    name: str = Field(alias="name_mi18n")
    hard_mode_name: str = Field(alias="hard_mode_name_mi18n")
    icon: str


class StarRailChallengePeakMobInfo(APIModel):
    """
    Represents information about a mob in the Star Rail Challenge Peak.

    Attributes:
        maze_id (int): The unique identifier for the maze.
        name (str): The name of the mob.
        monster_name (str): The name of the monster associated with the mob.
        monster_icon (str): The icon representing the monster.
    """

    maze_id: int
    name: str
    monster_name: str
    monster_icon: str


class StarRailChallengePeakBuff(APIModel):
    """
    Represents a buff in the Star Rail Challenge Peak.

    Attributes:
        id (int): The unique identifier for the buff.
        name_mi18n (str): The multilingual name of the buff.
        desc_mi18n (str): The multilingual description of the buff.
        icon (str): The icon representing the buff.
    """

    id: int
    name_mi18n: str
    desc_mi18n: str
    icon: str


class StarRailChallengePeakMobRecord(APIModel):
    """
    Represents a record of a mob in the Star Rail Challenge Peak.

    Attributes:
        maze_id (int): The unique identifier for the maze.
        has_challenge_record (bool): Indicates whether there is a challenge record for the mob.
        challenge_time (PartialTime): The time of the challenge.
        avatars (list[RogueCharacter]): The list of avatars used in the challenge.
        round_num (int): The number of rounds in the challenge.
        star_num (int): The number of stars earned in the challenge.
        is_fast (Optional[bool]): Indicates whether the challenge was completed quickly. Defaults to False.
    """

    maze_id: int
    has_challenge_record: bool
    challenge_time: Optional[PartialTime] = None
    avatars: list[RogueCharacter]
    round_num: int
    star_num: int
    is_fast: Optional[bool] = False


class StarRailChallengePeakBossRecord(StarRailChallengePeakMobRecord):
    """
    Represents a record of a boss in the Star Rail Challenge Peak.

    Attributes:
        buff (StarRailChallengePeakBuff): The buff associated with the boss.
        hard_mode (bool): Indicates whether the boss was challenged in hard mode.
        finish_color_medal (bool): Indicates whether the color medal was finished.
        challenge_peak_rank_icon_type (str): The type of the rank icon for the challenge peak.
        challenge_peak_rank_icon (str): The rank icon for the challenge peak.
        record_unique_key (str): The unique key for the boss record.
    """

    buff: StarRailChallengePeakBuff
    hard_mode: bool

    finish_color_medal: bool
    challenge_peak_rank_icon_type: str
    challenge_peak_rank_icon: str
    record_unique_key: str


class StarRailChallengePeakRecord(APIModel):
    """
    Represents a record of the Star Rail Challenge Peak.

    Attributes:
        group (StarRailChallengePeakGroup): The group information for the challenge peak.
        boss_info (StarRailChallengePeakBossInfo): Information about the boss in the challenge peak.
        mob_infos (list[StarRailChallengePeakMobInfo]): A list of mob information in the challenge peak.
        has_challenge_record (bool): Indicates whether there is a challenge record.
        battle_num (int): The number of battles in the challenge peak.
        boss_record (Optional[StarRailChallengePeakBossRecord]): The record of the boss in the challenge peak.
        mob_records (list[StarRailChallengePeakMobRecord]): A list of mob records in the challenge peak.
        boss_stars (int): The number of stars earned from the boss.
        mob_stars (int): The number of stars earned from the mobs.
    """

    group: StarRailChallengePeakGroup
    boss_info: StarRailChallengePeakBossInfo
    mob_infos: list[StarRailChallengePeakMobInfo]
    has_challenge_record: bool
    battle_num: int
    boss_record: Optional[StarRailChallengePeakBossRecord] = None
    mob_records: list[StarRailChallengePeakMobRecord]
    boss_stars: int
    mob_stars: int


class StarRailChallengePeakRankIconType(str, Enum):
    """
    Enumeration for the types of rank icons in the Star Rail Challenge Peak.
    """

    NONE = "ChallengePeakRankIconTypeNone"
    Ultra = "ChallengePeakRankIconTypeUltra"
    Gold = "ChallengePeakRankIconTypeGold"
    Silver = "ChallengePeakRankIconTypeSilver"
    Bronze = "ChallengePeakRankIconTypeBronze"


class StarRailChallengePeakBestRecordBrief(APIModel):
    """
    Represents a brief summary of the best record in the Star Rail Challenge Peak.

    Attributes:
        total_battle_num (int): The total number of battles.
        mob_stars (int): The number of stars earned from mobs.
        boss_stars (int): The number of stars earned from bosses.
        challenge_peak_rank_icon_type (str): The type of the rank icon for the challenge peak.
        challenge_peak_rank_icon (str): The rank icon for the challenge peak.
    """

    total_battle_num: int
    mob_stars: int
    boss_stars: int
    challenge_peak_rank_icon_type: StarRailChallengePeakRankIconType
    challenge_peak_rank_icon: str


class StarRailChallengePeakRole(APIModel):
    """
    Represents role information in the Star Rail Challenge Peak.

    Attributes:
        server (str): The server where the role is located.
        nickname (str): The nickname of the role.
        level (int): The level of the role.
        role_id (str): The unique identifier of the role.
    """

    server: str
    nickname: str
    level: int
    role_id: str


class StarRailChallengePeak(APIModel):
    """
    Represents the Star Rail Challenge Peak.

    Attributes:
        challenge_peak_records (list[StarRailChallengePeakRecord]): A list of challenge peak records.
        has_more_boss_record (bool): Indicates whether there are more boss records.
        challenge_peak_best_record_brief (StarRailChallengePeakBestRecordBrief): A brief summary of the best record in the challenge peak.
        role (StarRailChallengePeakRole): Information about the role in the challenge peak.
    """

    challenge_peak_records: list[StarRailChallengePeakRecord]
    has_more_boss_record: bool
    challenge_peak_best_record_brief: StarRailChallengePeakBestRecordBrief
    role: StarRailChallengePeakRole
