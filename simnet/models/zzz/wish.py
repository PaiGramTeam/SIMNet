from datetime import datetime
from enum import IntEnum, StrEnum
from typing import Any

from pydantic import field_validator

from simnet.models.base import APIModel, Field
from simnet.models.starrail.chronicle.base import PartialTime


class ZZZBannerTypeHoyolab(IntEnum):
    """Banner types in wish histories."""

    GACHA_TYPE_PERMANENT = 1
    """Permanent standard banner."""

    GACHA_TYPE_CHARACTER_UP = 2
    """Rotating character banner."""

    GACHA_TYPE_WEAPON_UP = 3
    """Rotating weapon banner."""

    GACHA_TYPE_BANGBOO = 5
    """BangBoo banner."""


class ZZZBannerType(IntEnum):
    """Banner types in wish histories."""

    STANDARD = PERMANENT = NOVICE = 1
    """Permanent standard banner."""

    CHARACTER = 2
    """Rotating character banner."""

    WEAPON = 3
    """Rotating weapon banner."""

    BANGBOO = 5
    """BangBoo banner."""


class ZZZWish(APIModel):
    """Wish made on any banner."""

    uid: int
    """User ID of the wish maker."""

    id: int
    """ID of the wished item."""

    type: str = Field(alias="item_type")
    """Type of the wished item."""

    item_id: int = Field(alias="item_id")
    """ID of the wished item."""

    name: str
    """Name of the wished item."""

    rarity: int = Field(alias="rank_type")
    """Rarity of the wished item."""

    time: datetime
    """Time when the wish was made."""

    banner_id: int = Field(alias="gacha_id")
    """ID of the banner the wish was made on."""

    banner_type: ZZZBannerType = Field(alias="gacha_type")
    """Type of the banner the wish was made on."""

    @field_validator("banner_type", mode="before")
    @classmethod
    def cast_banner_type(cls, v: Any) -> int:
        """Converts the banner type from any type to int."""
        return int(v)

    @field_validator("rarity")
    @classmethod
    def add_rarity(cls, v: int) -> int:
        """Add rarity 1."""
        return v + 1

    @classmethod
    def from_hoyolab(cls, data: dict, player_id: int, banner_type: int) -> "ZZZWish":
        item_type_enum = ZZZWishItemTypeHoyolab(data["item_type"])
        item_type = {
            ZZZWishItemTypeHoyolab.AGENT: "代理人",
            ZZZWishItemTypeHoyolab.SOUND_ENGINE: "音擎",
            ZZZWishItemTypeHoyolab.BANGBOO: "邦布",
        }[item_type_enum]
        rarity = {
            "S": 4,
            "A": 3,
            "B": 2,
        }[data["rarity"].upper()]
        time = PartialTime.model_validate(data["date"])
        return cls(
            uid=player_id,
            id=data["id"],
            item_type=item_type,
            item_id=data["item_id"],
            name=data["item_name"],
            rank_type=rarity,
            time=time.datetime,
            gacha_id=0,
            gacha_type=banner_type,
        )


class ZZZWishItemTypeHoyolab(StrEnum):
    """Types of items that can be wished for."""

    AGENT = "ITEM_TYPE_AVATAR"
    """Agent type item."""

    SOUND_ENGINE = "ITEM_TYPE_WEAPON"
    """Sound Engine type item."""

    BANGBOO = "ITEM_TYPE_BANGBOO"
    """BangBoo type item."""
