import re
from typing import Any, Optional, cast

from pydantic import ValidationInfo, field_validator

from simnet.models.base import APIModel, Field
from simnet.models.genshin.chronicle.abyss import SpiralAbyssPair
from simnet.models.genshin.chronicle.characters import PartialCharacter
from simnet.models.lab.record import UserInfo


class StatsRoleCombat(APIModel):
    """Role-based combat stats."""

    is_unlock: bool
    max_round_id: int
    has_data: bool
    has_detail_data: bool


class Stats(APIModel):
    """Overall user stats.

    Attributes:
        achievements (int): Number of achievements completed by the user.
        days_active (int): Number of days the user has been active.
        characters (int): Number of characters owned by the user.
        full_fetter_avatar_num (int): Number of characters with full fetters.
        spiral_abyss (str): The floor and level reached by the user in Spiral Abyss.
        anemoculi (int): Number of Anemoculus collected by the user.
        geoculi (int): Number of Geoculus collected by the user.
        dendroculi (int): Number of Dendroculus collected by the user.
        electroculi (int): Number of Electroculus collected by the user.
        hydroculi (int): Number of Hydroculus opened by the user.
        pyroculi (int): Number of Pyroculus opened by the user.
        common_chests (int): Number of Common Chests opened by the user.
        exquisite_chests (int): Number of Exquisite Chests opened by the user.
        precious_chests (int): Number of Precious Chests opened by the user.
        luxurious_chests (int): Number of Luxurious Chests opened by the user.
        remarkable_chests (int): Number of Magic Chests opened by the user.
        unlocked_waypoints (int): Number of waypoints unlocked by the user.
        unlocked_domains (int): Number of domains unlocked by the user.
    """

    achievements: int = Field(alias="achievement_number")
    days_active: int = Field(alias="active_day_number")
    characters: int = Field(alias="avatar_number")
    full_fetter_avatar_num: int
    spiral_abyss: str = Field(alias="spiral_abyss")

    anemoculi: int = Field(alias="anemoculus_number")
    geoculi: int = Field(alias="geoculus_number")
    dendroculi: int = Field(alias="dendroculus_number")
    electroculi: int = Field(alias="electroculus_number")
    hydroculi: int = Field(alias="hydroculus_number")
    pyroculi: int = Field(alias="pyroculus_number")

    common_chests: int = Field(alias="common_chest_number")
    exquisite_chests: int = Field(alias="exquisite_chest_number")
    precious_chests: int = Field(alias="precious_chest_number")
    luxurious_chests: int = Field(alias="luxurious_chest_number")
    remarkable_chests: int = Field(alias="magic_chest_number")
    unlocked_waypoints: int = Field(alias="way_point_number")
    unlocked_domains: int = Field(alias="domain_number")
    role_combat: StatsRoleCombat


class Offering(APIModel):
    """Exploration offering.

    Attributes:
        name (str): The name of the offering.
        level (int): The level of the offering.
        icon (str): The icon of the offering.
    """

    name: str
    level: int
    icon: str = ""


class Exploration(APIModel):
    """Exploration data.

    Attributes:
        id (int): The ID of the exploration.
        parent_id (int): The ID of the parent exploration.
        name (str): The name of the exploration.
        raw_explored (int): The raw percentage of the exploration completed.
        type (str): The type of the exploration.
        level (int): The level of the exploration.
        icon (str): The icon of the exploration.
        inner_icon (str): The inner icon of the exploration.
        background_image (str): The background image of the exploration.
        cover (str): The cover of the exploration.
        map_url (str): The URL of the exploration map.
        offerings (List[Offering]): The list of offerings of the exploration.
    """

    id: int
    parent_id: int
    name: str
    raw_explored: int = Field(alias="exploration_percentage")

    # deprecated in a sense:
    type: str
    level: int

    icon: str
    inner_icon: str
    background_image: str
    cover: str
    map_url: str

    offerings: list[Offering]

    @property
    def explored(self) -> float:
        """The percentage of the exploration completed.

        Returns:
            The percentage of the exploration completed.
        """
        return self.raw_explored / 10

    @field_validator("offerings", mode="before")
    @classmethod
    def add_base_offering(cls, offerings: list[Any], info: ValidationInfo) -> list[Any]:
        """Add a base offering if the exploration type is Reputation.

        Args:
            offerings (List[Any]): The list of offerings.
            info (ValidationInfo): The validation info.

        Returns:
            The updated list of offerings.
        """
        if info.data["type"] == "Reputation" and not any(info.data["type"] == o["name"] for o in offerings):
            offerings = [
                *offerings,
                {"name": info.data["type"], "level": info.data["level"]},
            ]

        return offerings


class TeapotRealm(APIModel):
    """A specific teapot realm.

    Attributes:
        name (str): The name of the teapot realm.
        icon (str): The icon of the teapot realm.
    """

    name: str
    icon: str

    @property
    def id(self) -> int:
        """The ID of the teapot realm.

        Returns:
            The ID of the teapot realm.
        """
        match = re.search(r"\d", self.icon)
        return int(match.group()) if match else 0


class Teapot(APIModel):
    """User's Serenitea Teapot.

    Attributes:
        realms (List[TeapotRealm]): The list of teapot realms of the user.
        level (int): The level of the teapot.
        visitors (int): The number of visitors to the teapot.
        comfort (int): The comfort level of the teapot.
        items (int): The number of items in the teapot.
        comfort_name (str): The name of the comfort level.
        comfort_icon (str): The icon of the comfort level.
    """

    realms: list[TeapotRealm]
    level: int
    visitors: int = Field(alias="visit_num")
    comfort: int = Field(alias="comfort_num")
    items: int = Field(alias="item_num")
    comfort_name: str = Field(alias="comfort_level_name")
    comfort_icon: str = Field(alias="comfort_level_icon")


class PartialGenshinUserStats(APIModel):
    """User stats with characters without equipment.

    Attributes:
        info (UserInfo): The user's information.
        stats (Stats): The user's stats.
        characters (List[PartialCharacter]): The list of the user's characters without equipment.
        explorations (List[Exploration]): The list of the user's explorations.
        teapot (Optional[Teapot]): The user's Serenitea Teapot.
    """

    info: UserInfo = Field(alias="role")
    stats: Stats
    characters: list[PartialCharacter] = Field(alias="avatars")
    explorations: list[Exploration] = Field(alias="world_explorations")
    teapot: Optional[Teapot] = Field(None, alias="homes")

    @field_validator("teapot", mode="before")
    @classmethod
    def format_teapot(cls, v: Any) -> Optional[dict[str, Any]]:
        """Format the user's Serenitea Teapot.

        Args:
            v (Any): The original value of the user's Serenitea Teapot.

        Returns:
            The formatted user's Serenitea Teapot.
        """
        if not v:
            return None
        if isinstance(v, dict):
            return cast("dict[str, Any]", v)
        return {**v[0], "realms": v}


class GenshinUserStats(PartialGenshinUserStats):
    """User stats with characters with equipment."""


class FullGenshinUserStats(GenshinUserStats):
    """User stats with all data a user can have.

    Attributes:
        abyss (SpiralAbyssPair): The user's Spiral Abyss data.
        activities (Dict): The user's activities data.
    """

    abyss: SpiralAbyssPair
    activities: dict
