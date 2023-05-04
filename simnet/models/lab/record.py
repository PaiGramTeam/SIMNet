import enum
import re
from typing import Optional, Any, Dict, List, Union

import pydantic


__all__ = (
    "FullUser",
    "Gender",
    "GenshinAccount",
    "UserCertification",
    "UserLevel",
    "PartialUser",
    "RecordCard",
    "RecordCardData",
    "RecordCardSetting",
    "RecordCardSettingType",
    "UserInfo",
)

from pydantic import Field

from simnet.models.base import APIModel
from simnet.utils.enum_ import Game


class GenshinAccount(APIModel):
    """Genshin account."""

    game_biz: str
    uid: int = Field(alias="game_uid")
    level: int
    nickname: str
    server: str = Field(alias="region")
    server_name: str = Field(alias="region_name")

    @property
    def game(self) -> Union[Game, str]:
        if "hk4e" in self.game_biz:
            return Game.GENSHIN
        elif "bh3" in self.game_biz:
            return Game.HONKAI
        elif "hkrpg" in self.game_biz:
            return Game.STARRAIL

        try:
            return Game(self.game_biz)
        except ValueError:
            return self.game_biz


class UserInfo(APIModel):
    """Chronicle user info."""

    nickname: str
    server: str = Field(alias="region")
    level: int
    icon: str = Field(alias="AvatarUrl")


class RecordCardData(APIModel):
    """Data entry of a record card."""

    name: str
    value: str


class RecordCardSetting(APIModel):
    """Privacy setting of a record card."""

    id: int = Field(alias="switch_id")
    description: str = Field(alias="switch_name")
    public: bool = Field(alias="is_public")


class RecordCardSettingType(enum.IntEnum):
    """Privacy setting of a record card."""

    SHOW_CHRONICLE = 1
    SHOW_CHARACTER_DETAILS = 2
    ENABLE_REAL_TIME_NOTES = 3


class Gender(enum.IntEnum):
    unknown = 0
    male = 1
    female = 2
    other = 3


class PartialUser(APIModel):
    """Partial user from a search result."""

    accident_id: int = Field(alias="uid")
    nickname: str
    introduction: str = Field(alias="introduce")
    avatar_id: int = Field(alias="avatar")
    gender: Gender
    icon: str = Field(alias="avatar_url")

    @pydantic.validator("nickname")
    def __remove_highlight(cls, v: str) -> str:
        return re.sub(r"<.+?>", "", v)


class UserCertification(APIModel):
    """user certification.

    For example artist's type is 2.
    """

    icon_url: Optional[str] = None
    description: Optional[str] = Field(alias="desc", default=None)
    type: int


class UserLevel(APIModel):
    """user level."""

    level: int
    exp: int
    level_desc: str
    bg_color: str
    bg_image: str


class FullUser(PartialUser):
    """Full user.

    Not actually full, but most of the data is useless.
    """

    certification: Optional[UserCertification] = None
    level: Optional[UserLevel] = None
    pendant_url: str = Field(alias="pendant")
    bg_url: Optional[str] = None
    pc_bg_url: Optional[str] = None


class RecordCard(GenshinAccount):
    """record card."""

    def __new__(cls, **kwargs: Any) -> "RecordCard":
        """Create the appropriate record card."""
        game_id = kwargs.get("game_id", 0)
        if game_id == 1:
            cls = HonkaiRecordCard
        elif game_id == 2:
            cls = GenshinRecordCard
        elif game_id == 6:
            cls = StarRailRecodeCard

        return super().__new__(cls)

    game_id: int
    game_biz: str = ""
    uid: int = Field(alias="game_role_id")

    data: List[RecordCardData]
    settings: List[RecordCardSetting] = Field(alias="data_switches")

    public: bool = Field(alias="is_public")
    background_image: str
    has_uid: bool = Field(alias="has_role")
    url: str

    def as_dict(self) -> Dict[str, Any]:
        """Return data as a dictionary."""
        return {
            d.name: (int(d.value) if d.value.isdigit() else d.value) for d in self.data
        }


class GenshinRecordCard(RecordCard):
    """Genshin record card."""

    @property
    def game(self) -> Game:
        return Game.GENSHIN

    @property
    def days_active(self) -> int:
        return int(self.data[0].value)

    @property
    def characters(self) -> int:
        return int(self.data[1].value)

    @property
    def achievements(self) -> int:
        return int(self.data[2].value)

    @property
    def spiral_abyss(self) -> str:
        return self.data[3].value


class HonkaiRecordCard(RecordCard):
    """Honkai record card."""

    @property
    def game(self) -> Game:
        return Game.HONKAI

    @property
    def days_active(self) -> int:
        return int(self.data[0].value)

    @property
    def stigmata(self) -> int:
        return int(self.data[1].value)

    @property
    def battlesuits(self) -> int:
        return int(self.data[2].value)

    @property
    def outfits(self) -> int:
        return int(self.data[3].value)


class StarRailRecodeCard(RecordCard):
    """Star rail record card."""

    @property
    def game(self) -> Game:
        return Game.STARRAIL

    @property
    def days_active(self) -> int:
        return int(self.data[0].value)

    @property
    def characters(self) -> int:
        return int(self.data[1].value)

    @property
    def achievements(self) -> int:
        return int(self.data[2].value)

    @property
    def chests(self) -> int:
        return int(self.data[3].value)
