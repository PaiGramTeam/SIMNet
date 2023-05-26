from datetime import datetime
from enum import IntEnum
from typing import Any

from pydantic import Field, validator

from simnet.models.base import APIModel


class StarRailBannerType(IntEnum):
    """Banner types in wish histories."""

    NOVICE = 2
    """Temporary novice banner."""

    STANDARD = PERMANENT = 1
    """Permanent standard banner."""

    CHARACTER = 11
    """Rotating character banner."""

    WEAPON = 12
    """Rotating weapon banner."""


class StarRailWish(APIModel):
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

    banner_type: StarRailBannerType = Field(alias="gacha_type")
    """Type of the banner the wish was made on."""

    @validator("banner_type", pre=True)
    def cast_banner_type(cls, v: Any) -> int:
        """Converts the banner type from any type to int."""
        return int(v)
