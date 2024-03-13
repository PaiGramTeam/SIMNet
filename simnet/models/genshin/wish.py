import re
from datetime import datetime
from enum import IntEnum
from typing import Any, Optional, List

from pydantic import Field, validator

from simnet.models.base import APIModel


class BannerType(IntEnum):
    """
    Enumeration of banner types in wish histories.

    Attributes:
        NOVICE (100): Temporary novice banner.
        STANDARD (200): Permanent standard banner.
        CHARACTER (301): Rotating character banner.
        WEAPON (302): Rotating weapon banner.
        CHARACTER1 (301): Special case, first character banner.
        CHARACTER2 (400): Special case, second character banner.
        CHRONICLED (500): Chronicled wish.
    """

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

    CHRONICLED = 500
    """Chronicled wish."""


class Wish(APIModel):
    """
    Model for a wish made on any banner.

    Attributes:
        uid (int): User ID.
        id (int): Wish ID.
        type (str): Item type.
        name (str): Item name.
        rarity (int): Item rarity.
        time (datetime): Wish timestamp.
        banner_type (BannerType): Type of banner.
        banner_name (str): Name of banner.
    """

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
        """Converts the banner type to an integer.

        Args:
            v (Any): The value to be validated.

        Returns:
            int: The validated integer value.
        """
        return int(v)


class BannerDetailItem(APIModel):
    """Represents an item that may be obtained from a banner.

    Attributes:
        name (str): The name of the item.
        type (str): The type of the item.
        rarity (int): The rarity of the item.
        up (bool): Whether the item has a rate-up on the current banner.
        order (int): The order value of the item.
    """

    name: str = Field(alias="item_name")
    type: str = Field(alias="item_type")
    rarity: int = Field(alias="rank")

    up: bool = Field(alias="is_up")
    order: int = Field(alias="order_value")


class BannerDetailsUpItem(APIModel):
    """Represents an item that has a rate-up on a banner.

    Attributes:
        name (str): The name of the item.
        type (str): The type of the item.
        element (str): The element of the item. Valid values are: "风", "火", "水", "雷", "冰", "岩", "草", "".
        icon (str): The URL of the item's icon.
    """

    name: str = Field(alias="item_name")
    type: str = Field(alias="item_type")
    element: str = Field(alias="item_attr")
    icon: str = Field(alias="item_img")

    @validator("element", pre=True)
    def parse_element(cls, v: str) -> str:
        """Converts the element string to a standardized format.

        Args:
            v (str): The value to be validated.

        Returns:
            str: The standardized element string.
        """
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
    """Details of a gacha banner.

    Attributes:
        banner_id (str): The unique ID of the banner.
        banner_type (int): The type of the banner.
            100: Novice Wishes
            200: Permanent Wish
            301: Character Event Wish
            302: Weapon Event Wish
            400: Character Event Wish
        title (str): The title of the banner.
        content (str): The description of the banner.
        date_range (str): The duration of the banner
            in the format of "YYYY-MM-DD HH:MM - YYYY-MM-DD HH:MM" in UTC timezone.
        r5_up_prob (float, optional): The probability of getting a 5-star item that is currently featured in the banner.
        r4_up_prob (float, optional): The probability of getting a 4-star item that is currently featured in the banner.
        r5_prob (float, optional): The probability of getting any 5-star item in the banner.
        r4_prob (float, optional): The probability of getting any 4-star item in the banner.
        r3_prob (float, optional): The probability of getting any 3-star item in the banner.
        r5_guarantee_prob (float, optional): The probability of getting a 5-star item after a certain number of pulls
            (pity system) in the banner.
        r4_guarantee_prob (float, optional): The probability of getting a 4-star item after a certain number of pulls
            (pity system) in the banner.
        r3_guarantee_prob (float, optional): The probability of getting a 3-star item after a certain number of pulls
            (pity system) in the banner.
        r5_up_items (List[BannerDetailsUpItem]): A list of featured 5-star items in the banner.
        r4_up_items (List[BannerDetailsUpItem]): A list of featured 4-star items in the banner.
        r5_items (List[BannerDetailItem]): A list of all 5-star items in the banner.
        r4_items (List[BannerDetailItem]): A list of all 4-star items in the banner.
        r3_items (List[BannerDetailItem]): A list of all 3-star items in the banner.
    """

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
    def replace_none(cls, v: Optional[List[Any]]) -> List[Any]:
        """Replaces NoneType attributes with an empty list.

        Args:
            v (Optional[List[Any]]): The input list.

        Returns:
            List[Any]: The input list with NoneType attributes replaced with an empty list.

        """
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
    def parse_percentage(cls, v: Optional[str]) -> Optional[float]:
        """Parses percentage strings into float values.

        Args:
            v (Optional[str]): The input string.

        Returns:
            Optional[float]: The float value of the input string, or None if the input is None or already a float.

        """
        if v is None or isinstance(v, (int, float)):
            return v

        return None if v == "0%" else float(v[:-1].replace(",", "."))

    @property
    def name(self) -> str:
        """Returns the name of the banner without HTML tags.

        Returns:
            str: The name of the banner.

        """
        return re.sub(r"<.*?>", "", self.title).strip()

    @property
    def banner_type_name(self) -> str:
        """Returns the name of the banner type based on the `banner_type` attribute.

        Returns:
            str: The name of the banner type.

        """
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
        """Returns a list of all items in the banner sorted by their order.

        Returns:
            List[BannerDetailItem]: A list of all items in the banner sorted by their order.

        """
        items = self.r5_items + self.r4_items + self.r3_items
        return sorted(items, key=lambda x: x.order)


class GachaItem(APIModel):
    """An item that can be obtained from a gacha pull.

    Attributes:
        name (str): The name of the item.
        type (str): The type of the item.
        rarity (int): The rarity of the item.
        id (int): The ID of the item.
    """

    name: str
    type: str = Field(alias="item_type")
    rarity: int = Field(alias="rank_type")
    id: int = Field(alias="item_id")

    @validator("id")
    def format_id(cls, v: int) -> int:
        """Formats the `id` attribute to a standardized 8-digit format.

        Args:
            v (int): The input ID.

        Returns:
            int: The formatted ID.

        """
        return 10000000 + v - 1000 if len(str(v)) == 4 else v

    def is_character(self) -> bool:
        """Returns whether the item is a character.

        Returns:
            bool: True if the item is a character, False otherwise.

        """
        return len(str(self.id)) == 8
