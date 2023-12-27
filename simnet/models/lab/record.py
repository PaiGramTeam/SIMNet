import enum
import re
from typing import Optional, Any, Dict, List, Union, Type

from pydantic import Field, validator

from simnet.models.base import APIModel
from simnet.utils.enums import Game

__all__ = (
    "FullUser",
    "Gender",
    "Account",
    "UserCertification",
    "UserLevel",
    "PartialUser",
    "RecordCard",
    "RecordCardData",
    "RecordCardSetting",
    "RecordCardSettingType",
    "UserInfo",
)


RECORD_CARD_MAP: Dict[int, Type["RecordCard"]] = {}


class Account(APIModel):
    """A representation of an account.

    Attributes:
        game_biz (str): The game business code for the account.
        uid (int): The game user ID associated with the account.
        level (int): The game level associated with the account.
        nickname (str): The game nickname associated with the account.
        server (str): The game server code associated with the account.
        server_name (str): The game server name associated with the account.
    """

    game_biz: str
    uid: int = Field(alias="game_uid")
    level: int
    nickname: str
    server: str = Field(alias="region")
    server_name: str = Field(alias="region_name")

    @property
    def game(self) -> Union[Game, str]:
        """Returns the game associated with the account.

        Returns:
            Union[Game, str]: The game associated with the account. If the game cannot be determined,
                the game business code is returned.
        """
        if "hk4e" in self.game_biz:
            return Game.GENSHIN
        if "bh3" in self.game_biz:
            return Game.HONKAI
        if "hkrpg" in self.game_biz:
            return Game.STARRAIL
        try:
            return Game(self.game_biz)
        except ValueError:
            return self.game_biz


class UserInfo(APIModel):
    """A representation of a user's information in a game.

    Attributes:
        nickname (str): The user's nickname in the game.
        server (str): The server code associated with the user.
        level (int): The user's level in the game.
        icon (str): The user's avatar URL.
    """

    nickname: str
    server: str = Field(alias="region")
    level: int
    icon: str = Field(alias="AvatarUrl")


class RecordCardData(APIModel):
    """A data entry of a record card.

    Attributes:
        name (str): The name of the data entry.
        value (str): The value of the data entry.
    """

    name: str
    value: str


class RecordCardSetting(APIModel):
    """A privacy setting of a record card.

    Attributes:
        id (int): The ID of the setting.
        description (str): The name of the setting.
        public (bool): Whether the setting is public or not.
    """

    id: int = Field(alias="switch_id")
    description: str = Field(alias="switch_name")
    public: bool = Field(alias="is_public")


class RecordCardSettingType(enum.IntEnum):
    """An enumeration of privacy setting types for a record card."""

    SHOW_CHRONICLE = 1
    SHOW_CHARACTER_DETAILS = 2
    ENABLE_REAL_TIME_NOTES = 3


class Gender(enum.IntEnum):
    """An enumeration of genders."""

    unknown = 0
    male = 1
    female = 2
    other = 3


class PartialUser(APIModel):
    """A representation of a partial user from a search result.

    Attributes:
        accident_id (int): The user's ID.
        nickname (str): The user's nickname.
        introduction (str): The user's introduction.
        avatar_id (int): The user's avatar ID.
        avatar_url (str): The user's avatar URL.
        gender (Gender): The user's gender.
        icon (str): The user's avatar URL.
    """

    accident_id: int = Field(alias="uid")
    nickname: str
    introduction: str = Field(alias="introduce")
    avatar_id: Optional[str] = Field(alias="avatar")
    avatar_url: Optional[str] = ""
    gender: Gender
    icon: str = Field(alias="avatar_url")

    @validator("nickname")
    def remove_highlight(cls, v: str) -> str:
        """Removes the highlight tags from the user's nickname.

        Args:
            v (str): The user's nickname.

        Returns:
            str: The user's nickname without any highlight tags.
        """
        return re.sub(r"<.+?>", "", v)


class UserCertification(APIModel):
    """A representation of a user's certification.

    Attributes:
        icon_url (Optional[str]): The certification's icon URL.
        description (Optional[str]): The certification's description.
        type (int): The certification's type, e.g. 2 for artist.
    """

    icon_url: Optional[str] = None
    description: Optional[str] = Field(alias="desc", default=None)
    type: int


class UserLevel(APIModel):
    """A representation of a user's level.

    Attributes:
        level (int): The user's level.
        exp (int): The user's experience points.
        level_desc (str): The user's level description.
        bg_color (str): The user's background color.
        bg_image (str): The user's background image.
    """

    level: int
    exp: int
    level_desc: str
    bg_color: str
    bg_image: str


class FullUser(PartialUser):
    """A representation of a full user.

    Attributes:
        certification (Optional[UserCertification]): The user's certification.
        level (Optional[UserLevel]): The user's level.
        pendant_url (str): The user's pendant URL.
        bg_url (Optional[str]): The user's background URL.
        pc_bg_url (Optional[str]): The user's PC background URL.
    """

    certification: Optional[UserCertification] = None
    level: Optional[UserLevel] = None
    pendant_url: str = Field(alias="pendant")
    bg_url: Optional[str] = None
    pc_bg_url: Optional[str] = None


class BaseRecordCard(Account):
    """A representation of a record card.

    Attributes:
        game_id (int): The ID of the game associated with the record card.
        game_biz (str): The game business code for the record card.
        uid (int): The game user ID associated with the record card.
        data (List[RecordCardData]): A list of data entries for the record card.
        settings (List[RecordCardSetting]): A list of privacy settings for the record card.
        public (bool): Whether the record card is public or not.
        background_image (str): The URL of the background image for the record card.
        has_uid (bool): Whether the record card has a user ID associated with it or not.
        url (str): The URL of the record card.
    """

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
        """Returns the data as a dictionary.

        Returns:
            Dict[str, Any]: The data as a dictionary.
        """
        return {d.name: (int(d.value) if d.value.isdigit() else d.value) for d in self.data}


class RecordCard(BaseRecordCard):
    """A representation of a record card.

    Attributes:
        game_id (int): The ID of the game associated with the record card.
        game_biz (str): The game business code for the record card.
        uid (int): The game user ID associated with the record card.
        data (List[RecordCardData]): A list of data entries for the record card.
        settings (List[RecordCardSetting]): A list of privacy settings for the record card.
        public (bool): Whether the record card is public or not.
        background_image (str): The URL of the background image for the record card.
        has_uid (bool): Whether the record card has a user ID associated with it or not.
        url (str): The URL of the record card.
    """

    @classmethod
    def creat(cls, **kwargs: Any):
        """Creates a record card.

        Args:
            **kwargs: Keyword arguments.

        Returns:
            RecordCard: The record card.
        """
        game_id = kwargs.get("game_id", 0)
        new_cls = RECORD_CARD_MAP.get(game_id, cls)
        return new_cls(**kwargs)


class GenshinRecordCard(RecordCard):
    """Genshin record card."""

    @property
    def game(self) -> Game:
        """Returns the game associated with the record card.

        Returns:
            Game: The game associated with the record card.
        """
        return Game.GENSHIN

    @property
    def days_active(self) -> int:
        """Returns the number of days the user has been active.

        Returns:
            int: The number of days the user has been active.
        """
        return int(self.data[0].value)

    @property
    def characters(self) -> int:
        """Returns the number of characters the user has.

        Returns:
            int: The number of characters the user has.
        """
        return int(self.data[1].value)

    @property
    def achievements(self) -> int:
        """Returns the number of achievements the user has.

        Returns:
            int: The number of achievements the user has.
        """
        return int(self.data[2].value)

    @property
    def spiral_abyss(self) -> str:
        """Returns the user's progress in the Spiral Abyss.

        Returns:
            str: The user's progress in the Spiral Abyss.
        """
        return self.data[3].value


class HonkaiRecordCard(RecordCard):
    """Honkai record card."""

    @property
    def game(self) -> Game:
        """Returns the game associated with the record card.

        Returns:
            Game: The game associated with the record card.
        """
        return Game.HONKAI

    @property
    def days_active(self) -> int:
        """Returns the number of days the user has been active.

        Returns:
            int: The number of days the user has been active.
        """
        return int(self.data[0].value)

    @property
    def stigmata(self) -> int:
        """Returns the number of stigmata the user has.

        Returns:
            int: The number of stigmata the user has.
        """
        return int(self.data[1].value)

    @property
    def battlesuits(self) -> int:
        """Returns the number of battlesuits the user has.

        Returns:
            int: The number of battlesuits the user has.
        """
        return int(self.data[2].value)

    @property
    def outfits(self) -> int:
        """Returns the number of outfits the user has.

        Returns:
            int: The number of outfits the user has.
        """
        return int(self.data[3].value)


class StarRailRecodeCard(RecordCard):
    """Star rail record card."""

    @property
    def game(self) -> Game:
        """Returns the game associated with the record card.

        Returns:
            Game: The game associated with the record card.
        """
        return Game.STARRAIL

    @property
    def days_active(self) -> int:
        """Returns the number of days the user has been active.

        Returns:
            int: The number of days the user has been active.
        """
        return int(self.data[0].value)

    @property
    def characters(self) -> int:
        """Returns the number of characters the user has.

        Returns:
            int: The number of characters the user has.
        """
        return int(self.data[1].value)

    @property
    def achievements(self) -> int:
        """Returns the number of achievements the user has.

        Returns:
            int: The number of achievements the user has.
        """
        return int(self.data[2].value)

    @property
    def chests(self) -> int:
        """Returns the number of chests the user has found.

        Returns:
            int: The number of chests the user has found.
        """
        return int(self.data[3].value)


RECORD_CARD_MAP.setdefault(1, HonkaiRecordCard)
RECORD_CARD_MAP.setdefault(2, GenshinRecordCard)
RECORD_CARD_MAP.setdefault(6, StarRailRecodeCard)
