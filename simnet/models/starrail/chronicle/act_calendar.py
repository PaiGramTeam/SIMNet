import datetime
from enum import Enum
from typing import List, Optional

from simnet.models.base import APIModel


class EquipListItem(APIModel):
    item_id: str
    item_name: str
    item_url: Optional[str] = ""
    rarity: int
    avatar_base_type: str
    is_forward: bool
    wiki_url: str


class AvatarListItem(EquipListItem):
    icon_url: str
    damage_type: int
    damage_type_name: str
    item_avatar_icon_path: str


class TimeInfo(APIModel):
    start_ts: datetime.datetime
    end_ts: datetime.datetime
    start_time: datetime.datetime
    end_time: datetime.datetime
    now: datetime.datetime


class CardPoolTypeEnum(str, Enum):
    Role = "CardPoolRole"
    Equipment = "CardPoolEquipment"


class CardPoolListItem(APIModel):
    id: str
    name: str
    type: CardPoolTypeEnum
    avatar_list: List[AvatarListItem]
    equip_list: List[EquipListItem]
    is_after_version: bool
    time_info: TimeInfo
    version: str


class RewardItem(APIModel):
    item_id: int
    name: str
    icon: str
    wiki_url: str
    num: int
    rarity: str


class ActTypeEnum(str, Enum):

    Sign = "ActivityTypeSign"
    Double = "ActivityTypeDouble"
    Other = "ActivityTypeOther"


class ActStatusEnum(str, Enum):

    SignStatusUnopened = "SignStatusUnopened"
    SignStatusUnSignedToday = "SignStatusUnSignedToday"
    SignStatusSignedToday = "SignStatusSignedToday"
    SignStatusUnclaimed = "SignStatusUnclaimed"
    SignStatusFinish = "SignStatusFinish"

    DoubleRewardActStatusUnopened = "DoubleRewardActStatusUnopened"
    DoubleRewardActStatusProgress = "DoubleRewardActStatusProgress"
    DoubleRewardActStatusFinish = "DoubleRewardActStatusFinish"

    OtherActStatusUnopened = "OtherActStatusUnopened"
    OtherActStatusUnFinish = "OtherActStatusUnFinish"
    OtherActStatusFinish = "OtherActStatusFinish"


class ActListItem(APIModel):
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


class ChallengeTypeEnum(str, Enum):
    Chasm = "ChallengeTypeChasm"
    Story = "ChallengeTypeStory"
    Boss = "ChallengeTypeBoss"


class ChallengeStatusEnum(str, Enum):
    Unopened = "challengeStatusUnopened"
    Progress = "challengeStatusInProgress"
    Finish = "challengeStatusFinish"


class ChallengeListItem(APIModel):
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
    avatar_card_pool_list: List[CardPoolListItem]
    equip_card_pool_list: List[CardPoolListItem]
    act_list: List[ActListItem]
    challenge_list: List[ChallengeListItem]
    now: datetime.datetime
    cur_game_version: str
