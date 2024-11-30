from enum import Enum
from typing import List, Optional

from simnet.models.base import APIModel, DateTimeField


class EquipListItem(APIModel):
    """A model representing an equipment item in the StarRail act calendar."""

    item_id: str
    item_name: str
    item_url: Optional[str] = ""
    rarity: int
    avatar_base_type: str
    is_forward: bool
    wiki_url: str


class AvatarListItem(EquipListItem):
    """A model representing an avatar item in the StarRail act calendar."""

    icon_url: str
    damage_type: int
    damage_type_name: str
    item_avatar_icon_path: str


class TimeInfo(APIModel):
    """A model representing time information in the StarRail act calendar."""

    start_ts: DateTimeField
    end_ts: DateTimeField
    start_time: str
    end_time: str
    now: DateTimeField


class CardPoolTypeEnum(str, Enum):
    """An enumeration class representing the type of card pool in the StarRail act calendar."""

    Role = "CardPoolRole"
    Equipment = "CardPoolEquipment"


class CardPoolListItem(APIModel):
    """A model representing an item in the card pool list in the StarRail act calendar."""

    id: str
    name: str
    type: CardPoolTypeEnum
    avatar_list: List[AvatarListItem]
    equip_list: List[EquipListItem]
    is_after_version: bool
    time_info: TimeInfo
    version: str


class RewardItem(APIModel):
    """A model representing a reward item in the StarRail act calendar."""

    item_id: int
    name: str
    icon: str
    wiki_url: str
    num: int
    rarity: str


class ActTypeEnum(str, Enum):
    """An enumeration class representing the type of act in the StarRail act calendar."""

    Sign = "ActivityTypeSign"
    Double = "ActivityTypeDouble"
    RogueTourn = "ActivityTypeRogueTourn"
    Other = "ActivityTypeOther"


class ActStatusEnum(str, Enum):
    """An enumeration class representing the status of an act in the StarRail act calendar."""

    SignStatusUnopened = "SignStatusUnopened"
    SignStatusUnSignedToday = "SignStatusUnSignedToday"
    SignStatusSignedToday = "SignStatusSignedToday"
    SignStatusUnclaimed = "SignStatusUnclaimed"
    SignStatusFinish = "SignStatusFinish"

    DoubleRewardActStatusUnopened = "DoubleRewardActStatusUnopened"
    DoubleRewardActStatusProgress = "DoubleRewardActStatusProgress"
    DoubleRewardActStatusFinish = "DoubleRewardActStatusFinish"

    RogueTournActStatusProgress = "RogueTournActStatusProgress"

    OtherActStatusUnopened = "OtherActStatusUnopened"
    OtherActStatusUnFinish = "OtherActStatusUnFinish"
    OtherActStatusFinish = "OtherActStatusFinish"


class ActTimeTypeEnum(str, Enum):
    """An enumeration class representing the time type of an act in the StarRail act calendar."""

    Default = "ActTimeTypeDefault"
    Long = "ActTimeTypeLong"


class ActListItem(APIModel):
    """A model representing an item in the StarRail act calendar."""

    id: int
    version: str
    name: str
    act_type: ActTypeEnum
    act_status: ActStatusEnum
    reward_list: List[RewardItem]
    total_progress: int
    current_progress: int
    time_info: TimeInfo
    panel_id: int
    panel_desc: str
    strategy: str
    multiple_drop_type: int
    multiple_drop_type_list: List[int]
    count_refresh_type: int
    count_value: int
    drop_multiple: int
    is_after_version: bool
    sort_weight: int
    special_reward: RewardItem
    all_finished: bool
    show_text: str
    act_time_type: ActTimeTypeEnum


class ChallengeTypeEnum(str, Enum):
    """An enumeration class representing the type of challenge in the StarRail act calendar."""

    Chasm = "ChallengeTypeChasm"
    Story = "ChallengeTypeStory"
    Boss = "ChallengeTypeBoss"


class ChallengeStatusEnum(str, Enum):
    """An enumeration class representing the status of a challenge in the StarRail act calendar."""

    Unopened = "challengeStatusUnopened"
    Progress = "challengeStatusInProgress"
    Finish = "challengeStatusFinish"


class ChallengeListItem(APIModel):
    """A model representing a challenge item in the StarRail act calendar."""

    group_id: int
    name_mi18n: str
    challenge_type: ChallengeTypeEnum

    total_progress: int
    current_progress: int
    status: ChallengeStatusEnum

    time_info: TimeInfo
    reward_list: List[RewardItem]
    special_reward: RewardItem
    show_text: str


class StarRailActCalendar(APIModel):
    """A model representing the StarRail act calendar."""

    avatar_card_pool_list: List[CardPoolListItem]
    equip_card_pool_list: List[CardPoolListItem]
    act_list: List[ActListItem]
    challenge_list: List[ChallengeListItem]
    now: DateTimeField
    cur_game_version: str
