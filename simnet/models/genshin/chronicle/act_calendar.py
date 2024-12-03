from datetime import datetime

from simnet.models.base import APIModel, TimeDeltaField
from simnet.models.genshin.character import BaseCharacter


class EquipListItem(BaseCharacter):
    """A model representing an equipment item in the Genshin act calendar."""

    wiki_url: str


class AvatarListItem(BaseCharacter):
    """A model representing an avatar item in the Genshin act calendar."""

    is_invisible: bool = False


class CardPoolListItem(APIModel):
    """A model representing an item in the card pool list in the Genshin act calendar."""

    pool_id: int
    version_name: str
    pool_name: str
    pool_type: int
    avatars: list[AvatarListItem]
    weapon: list[EquipListItem]
    start_timestamp: datetime
    end_timestamp: datetime
    jump_url: str
    pool_status: int
    countdown_seconds: TimeDeltaField


class RewardItem(APIModel):
    """A model representing a reward item in the Genshin act calendar."""

    item_id: int
    name: str
    icon: str
    wiki_url: str
    num: int
    rarity: str
    homepage_show: bool


class ActListItem(APIModel):
    """A model representing an item in the Genshin act calendar."""

    id: int
    name: str
    type: str
    start_timestamp: datetime
    end_timestamp: datetime
    desc: str
    strategy: str
    countdown_seconds: TimeDeltaField
    status: int
    reward_list: list[RewardItem]
    is_finished: bool


class GenshinActCalendar(APIModel):
    """A model representing the StarRail act calendar."""

    avatar_card_pool_list: list[CardPoolListItem]
    weapon_card_pool_list: list[CardPoolListItem]
    mixed_card_pool_list: list[CardPoolListItem]

    act_list: list[ActListItem]
    fixed_act_list: list[ActListItem]
