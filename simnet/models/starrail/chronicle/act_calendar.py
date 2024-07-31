import datetime
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


class CardPoolListItem(APIModel):
    id: str
    name: str
    type: str
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


class ActListItem(APIModel):
    id: int
    version: str
    name: str
    act_type: str
    act_status: str
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


class ChallengeListItem(APIModel):
    group_id: int
    name_mi18n: str
    challenge_type: str

    total_progress: int
    current_progress: int
    status: str

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
