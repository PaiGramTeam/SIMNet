import re
from datetime import datetime
from enum import IntEnum
from typing import Any, Optional, List

from pydantic import Field, validator

from simnet.models.base import APIModel


class BannerType(IntEnum):
    """Banner types in wish histories."""

    NOVICE = 100
    """Temporary novice banner."""

    STANDARD = PERMANENT = 200
    """Permanent standard banner."""

    CHARACTER = 301
    """Rotating character banner."""

    WEAPON = 302
    """Rotating weapon banner."""

    # these are special cases
    # they exist inside the history but should be counted as the same

    CHARACTER1 = 301
    """Character banner #1."""

    CHARACTER2 = 400
    """Character banner #2."""


class Wish(APIModel):
    """Wish made on any banner."""

    uid: int

    id: int
    type: str = Field(alias="item_type")
    name: str
    rarity: int = Field(alias="rank_type")
    time: datetime

    banner_type: BannerType = Field(alias="gacha_type")
    banner_name: str

    @validator("banner_type", pre=True)
    def cast_banner_type(cls, v: Any) -> int:
        return int(v)


class BannerDetailItem(APIModel):
    """Item that may be gotten from a banner."""

    name: str = Field(alias="item_name")
    type: str = Field(alias="item_type")
    rarity: int = Field(alias="rank")

    up: bool = Field(alias="is_up")
    order: int = Field(alias="order_value")


class BannerDetailsUpItem(APIModel):
    """Item that has a rate-up on a banner."""

    name: str = Field(alias="item_name")
    type: str = Field(alias="item_type")
    element: str = Field(alias="item_attr")
    icon: str = Field(alias="item_img")

    @validator("element", pre=True)
    def parse_element(cls, v: str) -> str:
        return {
            "风": "Anemo",
            "火": "Pyro",
            "水": "Hydro",
            "雷": "Electro",
            "冰": "Cryo",
            "岩": "Geo",
            "草": "Dendro",
            "": "",
        }.get(v, v)


class BannerDetails(APIModel):
    """Details of a banner."""

    banner_id: str
    banner_type: int = Field(alias="gacha_type")
    title: str
    content: str
    date_range: str

    r5_up_prob: Optional[float]
    r4_up_prob: Optional[float]
    r5_prob: Optional[float]
    r4_prob: Optional[float]
    r3_prob: Optional[float]
    r5_guarantee_prob: Optional[float] = Field(alias="r5_baodi_prob")
    r4_guarantee_prob: Optional[float] = Field(alias="r4_baodi_prob")
    r3_guarantee_prob: Optional[float] = Field(alias="r3_baodi_prob")

    r5_up_items: List[BannerDetailsUpItem]
    r4_up_items: List[BannerDetailsUpItem]

    r5_items: List[BannerDetailItem] = Field(alias="r5_prob_list")
    r4_items: List[BannerDetailItem] = Field(alias="r4_prob_list")
    r3_items: List[BannerDetailItem] = Field(alias="r3_prob_list")

    @validator("r5_up_items", "r4_up_items", pre=True)
    def __replace_none(cls, v: Optional[List[Any]]) -> List[Any]:
        return v or []

    @validator(
        "r5_up_prob",
        "r4_up_prob",
        "r5_prob",
        "r4_prob",
        "r3_prob",
        "r5_guarantee_prob",
        "r4_guarantee_prob",
        "r3_guarantee_prob",
        pre=True,
    )
    def __parse_percentage(cls, v: Optional[str]) -> Optional[float]:
        if v is None or isinstance(v, (int, float)):
            return v

        return None if v == "0%" else float(v[:-1].replace(",", "."))

    @property
    def name(self) -> str:
        return re.sub(r"<.*?>", "", self.title).strip()

    @property
    def banner_type_name(self) -> str:
        banners = {
            100: "Novice Wishes",
            200: "Permanent Wish",
            301: "Character Event Wish",
            302: "Weapon Event Wish",
            400: "Character Event Wish",
        }
        return banners[self.banner_type]

    @property
    def items(self) -> List[BannerDetailItem]:
        items = self.r5_items + self.r4_items + self.r3_items
        return sorted(items, key=lambda x: x.order)


class GachaItem(APIModel):
    """Item that can be gotten from the gacha."""

    name: str
    type: str = Field(alias="item_type")
    rarity: int = Field(alias="rank_type")
    id: int = Field(alias="item_id")

    @validator("id")
    def format_id(cls, v: int) -> int:
        return 10000000 + v - 1000 if len(str(v)) == 4 else v

    def is_character(self) -> bool:
        """Whether this item is a charact"""
        return len(str(self.id)) == 8
