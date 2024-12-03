from typing import List

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
    difficulty: int
    exist_data: bool

    @property
    def floor(self) -> int:
        """Get the floor from the area ID."""
        return self.area_id % 10


class StarRailRogueTournRecordBrief(APIModel):
    """StarRail Rogue Tourn Record Brief"""

    title: str
    icon: str
    color: str
    common_info: StarRailRogueTournCommonInfo

    @property
    def exist_data(self) -> bool:
        """Check if the record exists."""
        return self.common_info.exist_data


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


class StarRailRogueTournRecord(APIModel):
    """Star Rail Rogue Tourn Record"""

    finish_time: PartialTime
    final_lineup: List[RogueCharacter]
    base_type_list: List[RogueBuffType]
    buffs: List[RogueBuff]
    miracles: List[RogueTournMiracle]
    hex_miracles: List[RogueTournMiracle]
    formula_list: List[RogueTournFormula]
    common_info: StarRailRogueTournCommonInfo


class StarRailRogueTournDetail(APIModel):
    """Star Rail Rogue Tourn Detail"""

    challenge_id: int
    weekly_name: str
    weekly_buff_desc: List[str]
    weekly_challenge_counts: int
    records: List[StarRailRogueTournRecord]


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
