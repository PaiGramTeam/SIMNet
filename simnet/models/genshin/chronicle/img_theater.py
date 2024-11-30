import datetime
import enum
import typing
from typing import Optional

from simnet.models.base import APIModel, Field, DateTimeField
from simnet.models.genshin.character import BaseCharacter
from simnet.models.starrail.chronicle.base import PartialTime
from simnet.models.zzz.calculator import desc_to_html


class TheaterCharaType(enum.IntEnum):
    """The type of character in the context of the imaginarium theater gamemode."""

    NORMAL = 1
    TRIAL = 2
    SUPPORT = 3


class TheaterDifficulty(enum.IntEnum):
    """The difficulty of the imaginarium theater data."""

    NULL = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    VISIONARY = 4


class ActCharacter(BaseCharacter):
    """A character in an act."""

    id: int = Field(alias="avatar_id")
    icon: str = Field(alias="image")
    avatar_type: TheaterCharaType
    level: int


class TheaterBuff(APIModel):
    """Represents either a 'mystery cache' or a 'wondrous boom'."""

    name: str
    icon: str
    desc: str
    is_enhanced: typing.Optional[bool] = False
    id: typing.Optional[int] = None

    @property
    def desc_html(self) -> str:
        return desc_to_html(self.desc)


class TheaterEnemy(APIModel):
    """
    Represents an enemy in the imaginarium theater.

    Attributes:
        name (str): The name of the enemy.
        icon (str): The icon representing the enemy.
        level (int): The level of the enemy.
    """

    name: str
    icon: str
    level: int


class TheaterSplendourBuffSummary(APIModel):
    """
    Represents a summary of the Theater Splendour Buff.

    Attributes:
        total_level (int): The total level of the buff.
        desc (str): The description of the buff.
    """

    total_level: int
    desc: str

    @property
    def desc_html(self) -> str:
        """
        Converts the description to HTML format.

        Returns:
            str: The HTML formatted description.
        """
        return desc_to_html(self.desc)


class TheaterSplendourBuffModel(APIModel):
    """
    Represents a model for the Theater Splendour Buff.

    Attributes:
        name (str): The name of the buff.
        icon (str): The icon representing the buff.
        level (int): The level of the buff.
        level_effect (typing.Sequence[TheaterBuff]): The effects of the buff at different levels.
    """

    name: str
    icon: str
    level: int
    level_effect: typing.Sequence[TheaterBuff]


class TheaterSplendourBuff(APIModel):
    """
    Represents the Theater Splendour Buff.

    Attributes:
        summary (TheaterSplendourBuffSummary): A summary of the Theater Splendour Buff.
        buffs (typing.Sequence[TheaterSplendourBuffModel]): A sequence of Theater Splendour Buff models.
    """

    summary: TheaterSplendourBuffSummary
    buffs: typing.Sequence[TheaterSplendourBuffModel]


class Act(APIModel):
    """One act in the theater."""

    avatars: typing.Sequence[ActCharacter]
    choice_cards: typing.Sequence[TheaterBuff]
    buffs: typing.Sequence[TheaterBuff]
    is_get_medal: bool
    round_id: int
    finish_time: DateTimeField
    finish_date_time: PartialTime
    enemies: typing.Optional[typing.Sequence[TheaterEnemy]] = None
    splendour_buff: typing.Optional[TheaterSplendourBuff] = None


class TheaterStats(APIModel):
    """Imaginarium theater stats."""

    difficulty: TheaterDifficulty = Field(alias="difficulty_id")
    """The difficulty"""
    max_round_id: int
    """The maximum act the player has reached."""
    heraldry: int  # Not sure what this is
    star_challenge_stellas: typing.Sequence[bool] = Field(alias="get_medal_round_list")
    """Whether the player has obtained the medal for each act."""
    medal_num: int
    """The number of medals the player has obtained."""
    coin_num: int
    """The number of Fantasia Flowers used."""
    audience_support_trigger_num: int = Field(alias="avatar_bonus_num")
    """The number of external audience support triggers."""
    rent_cnt: int
    """The number of supporting cast characters assisting other players."""


class TheaterSchedule(APIModel):
    """Imaginarium theater schedule."""

    start_time: DateTimeField
    end_time: DateTimeField
    schedule_type: int  # Not sure what this is
    id: int = Field(alias="schedule_id")
    start_date_time: PartialTime
    end_date_time: PartialTime


class ImgTheaterFightStaticAvatar(BaseCharacter):
    id: int = Field(alias="avatar_id")
    icon: str = Field(alias="avatar_icon")
    value: str


class ImgTheaterFightStatic(APIModel):
    max_defeat_avatar: Optional[ImgTheaterFightStaticAvatar] = None
    max_damage_avatar: Optional[ImgTheaterFightStaticAvatar] = None
    max_take_damage_avatar: Optional[ImgTheaterFightStaticAvatar] = None
    total_coin_consumed: Optional[ImgTheaterFightStaticAvatar] = None
    shortest_avatar_list: typing.Sequence[ImgTheaterFightStaticAvatar]
    total_use_time: int
    is_show_battle_stats: bool


class ImgTheaterDetailData(APIModel):
    """Imaginarium theater detail data."""

    rounds_data: typing.Sequence[Act]
    detail_stat: TheaterStats
    backup_avatars: typing.Sequence[ActCharacter]
    fight_statisic: typing.Optional[ImgTheaterFightStatic] = None


class ImgTheaterData(APIModel):
    """Imaginarium theater data."""

    detail: typing.Optional[ImgTheaterDetailData] = None
    stat: TheaterStats
    schedule: TheaterSchedule
    has_data: bool
    has_detail_data: bool


class ImgTheater(APIModel):
    """Imaginarium theater."""

    data: typing.List[ImgTheaterData]
    unlocked: bool = Field(alias="is_unlock")
