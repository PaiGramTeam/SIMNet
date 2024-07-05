from datetime import datetime
from enum import IntEnum
from typing import Any

from pydantic import Field, validator

from simnet.models.base import APIModel


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

    @validator("banner_type", pre=True)
    def cast_banner_type(cls, v: Any) -> int:
        """Converts the banner type from any type to int."""
        return int(v)

    @validator("rarity")
    def add_rarity(cls, v: int) -> int:
        """Add rarity 1."""
        return v + 1
