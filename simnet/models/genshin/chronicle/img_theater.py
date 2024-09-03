import datetime
import enum
import typing

from pydantic import Field

from simnet.models.base import APIModel
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

    icon: str
    name: str
    desc: str
    is_enhanced: bool
    id: int

    @property
    def desc_html(self) -> str:
        return desc_to_html(self.desc)


class Act(APIModel):
    """One act in the theater."""

    avatars: typing.Sequence[ActCharacter]
    choice_cards: typing.Sequence[TheaterBuff]
    buffs: typing.Sequence[TheaterBuff]
    is_get_medal: bool
    round_id: int
    finish_time: datetime.datetime
    finish_date_time: PartialTime


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

    start_time: datetime.datetime
    end_time: datetime.datetime
    schedule_type: int  # Not sure what this is
    id: int = Field(alias="schedule_id")
    start_date_time: PartialTime
    end_date_time: PartialTime


class ImgTheaterDetailData(APIModel):
    """Imaginarium theater detail data."""

    rounds_data: typing.Sequence[Act]
    backup_avatars: typing.Sequence[ActCharacter]
    detail_stat: TheaterStats


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
