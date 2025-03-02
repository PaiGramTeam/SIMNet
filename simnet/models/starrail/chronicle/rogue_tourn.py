from typing import Optional

from simnet.models.base import APIModel
from simnet.models.starrail.character import RogueCharacter
from simnet.models.starrail.chronicle.base import PartialTime
from simnet.models.starrail.chronicle.rogue import (
    RogueBuff,
    RogueBuffType,
    RogueMiracle,
    RogueUserRole,
)


class StarRailRogueTournCommonInfo(APIModel):
    """Star Rail Tourn Common Info"""

    area_id: int
    difficulty: Optional[int] = 0
    exist_data: bool

    @property
    def floor(self) -> int:
        """Get the floor from the area ID."""
        return self.area_id % 10


class StarRailRogueTournCommonInfoV2(StarRailRogueTournCommonInfo):
    """
    Represents the version 2 of the common information for the Star Rail Rogue Tournament.

    Attributes:
    - level (int): The level of the tournament.
    - id (int): The unique identifier for the tournament.
    """

    level: int
    id: int


class StarRailRogueTournRecordBrief(APIModel):
    """StarRail Rogue Tourn Record Brief"""

    title: str
    icon: str
    color: Optional[str] = None
    common_info: Optional[StarRailRogueTournCommonInfo] = None
    common_info_v2: Optional[StarRailRogueTournCommonInfoV2] = None

    @property
    def exist_data(self) -> bool:
        """Check if the record exists."""
        if self.common_info:
            return self.common_info.exist_data
        if self.common_info_v2:
            return self.common_info_v2.exist_data
        return False


class StarRailRogueTournBasicSeason(APIModel):
    """
    Represents the basic season information for the Star Rail Rogue Tournament.

    Attributes:
    - season_id (int): The unique identifier for the season.
    - season_level (int): The level of the season.
    - season_name (str): The name of the season.
    - icon (str): The icon representing the season.
    """

    season_id: int
    season_level: int
    season_name: str
    icon: str


class StarRailRogueTournBasic(APIModel):
    """Star Rail Rogue Tourn Basic"""

    season_level: int
    weekly_score: int
    weekly_score_max: int
    possibility_gallery_progress: int
    skill_tree_activated: int
    season_task_total: int
    season_task_finished: int
    normal_record_brief: StarRailRogueTournRecordBrief
    weekly_record_brief: StarRailRogueTournRecordBrief
    finished_weekly: bool
    rogue_tourn_exp_is_full: Optional[bool] = False
    titan_total: Optional[int] = None
    titan_current: Optional[int] = None
    season_title_list: Optional[list[StarRailRogueTournBasicSeason]] = None


class RogueTournMiracle(RogueMiracle):
    """Star Rail Rogue Tourn Miracle"""

    rank: int


class RogueTournFormula(APIModel):
    """Star Rail Rogue Tourn Formula"""

    id: int
    icon: str
    sub_icon: str
    name: str
    formula_category: int


class RogueTournTitanBless(APIModel):
    """
    Represents a Titan Blessing in the Star Rail Rogue Tournament.

    Attributes:
    - id (int): The unique identifier for the Titan Blessing.
    - name (str): The name of the Titan Blessing.
    - icon (str): The icon representing the Titan Blessing.
    - rarity (int): The rarity level of the Titan Blessing.
    - type (int): The type category of the Titan Blessing.
    """

    id: int
    name: str
    icon: str
    rarity: int
    type: int


class StarRailRogueTournRecord(APIModel):
    """Star Rail Rogue Tourn Record"""

    finish_time: PartialTime
    final_lineup: list[RogueCharacter]
    base_type_list: list[RogueBuffType]
    buffs: list[RogueBuff]
    miracles: list[RogueTournMiracle]
    hex_miracles: list[RogueTournMiracle]
    formula_list: list[RogueTournFormula]
    common_info: Optional[StarRailRogueTournCommonInfo] = None
    easy_mode: Optional[int] = None
    rank_mode: Optional[str] = None
    titan_bless_list: Optional[list[RogueTournTitanBless]] = None
    common_info_v2: Optional[StarRailRogueTournCommonInfoV2] = None


class StarRailRogueTournDetail(APIModel):
    """Star Rail Rogue Tourn Detail"""

    challenge_id: int
    weekly_name: str
    weekly_buff_desc: list[str]
    weekly_challenge_counts: int
    records: list[StarRailRogueTournRecord]


class StarRailRogueTourn(APIModel):
    """
    Star Rail Rogue Tourn class represents the main data structure for the Star Rail Rogue Tournament.

    Attributes:
    - basic: StarRailRogueTournBasic object containing basic information about the player's progress.
    - normal_detail: StarRailRogueTournDetail object containing detailed information about the normal challenge.
    - cur_week_detail: StarRailRogueTournDetail object containing detailed information about the current week's challenge.
    - last_week_detail: StarRailRogueTournDetail object containing detailed information about the last week's challenge.
    - role: RogueUserRole object representing the player's role in the tournament.

    Methods:
    None (This class only contains attributes and does not have any methods.)
    """

    basic: StarRailRogueTournBasic
    normal_detail: StarRailRogueTournDetail
    cur_week_detail: StarRailRogueTournDetail
    last_week_detail: StarRailRogueTournDetail
    role: RogueUserRole
