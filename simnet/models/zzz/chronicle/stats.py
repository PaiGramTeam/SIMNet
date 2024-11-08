"""Starrail chronicle stats."""

import typing

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.zzz import character


class ZZZStatsCommemorativeCoin(APIModel):
    """A data model representing commemorative coins for ZZZ stats."""

    num: int
    name: str
    sort: int


class ZZZStats(APIModel):
    """Overall user stats."""

    active_days: int
    avatar_num: int
    world_level_name: str
    cur_period_zone_layer_count: int
    buddy_num: int
    commemorative_coins_list: typing.Sequence[ZZZStatsCommemorativeCoin]
    achievement_count: int
    climbing_tower_layer: int
    next_hundred_layer: str


class ZZZAvatarBasic(APIModel):
    """Basic avatar"""

    characters: typing.Sequence[character.ZZZPartialCharacter] = Field(alias="avatar_list")


class ZZZBuddyBasic(APIModel):
    """Basic buddy"""

    buddy_list: typing.Sequence[character.ZZZPartialBuddy] = Field(alias="list")


class ZZZCatNote(APIModel):
    """
    A data model representing a category of ZZZ notes.

    Args:
        id (int): The ID of the category.
        name (str): The name of the category.
        icon (str): The icon associated with the category.
        num (int): The number of notes in the category.
        total (int): The total number of notes in the category.
        is_lock (bool): A boolean indicating if the category is locked.
    """

    id: int
    name: str
    icon: str
    num: int
    total: int
    is_lock: bool


class ZZZGameDataShow(APIModel):
    """
    Represents the game data display information.

    Attributes:
        personal_title (str): The personal title of the user.
        title_main_color (str): The main color of the title.
        title_bottom_color (str): The bottom color of the title.
        title_bg_url (str): The background URL of the title.
        medal_list (typing.Sequence[str]): A list of medals.
        card_url (str): The URL of the card.
    """

    personal_title: str
    title_main_color: str
    title_bottom_color: str
    title_bg_url: str

    medal_list: typing.Sequence[str]
    card_url: str


class ZZZUserStats(ZZZAvatarBasic):
    """User stats with characters without equipment."""

    stats: ZZZStats
    cur_head_icon_url: str
    buddy_list: typing.Sequence[character.ZZZPartialBuddy]
    cat_notes_list: typing.Sequence[ZZZCatNote]
    game_data_show: ZZZGameDataShow
