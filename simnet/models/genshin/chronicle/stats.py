import re
from typing import Any, Optional, cast, List, Dict

from pydantic import validator, Field

from simnet.models.base import APIModel
from simnet.models.genshin.chronicle.abyss import SpiralAbyssPair
from simnet.models.genshin.chronicle.characters import PartialCharacter, Character
from simnet.models.lab.record import UserInfo


class Stats(APIModel):
    """Overall user stats."""

    achievements: int = Field(alias="achievement_number")
    days_active: int = Field(alias="active_day_number")
    characters: int = Field(alias="avatar_number")
    spiral_abyss: str = Field(alias="spiral_abyss")
    anemoculi: int = Field(alias="anemoculus_number")
    geoculi: int = Field(alias="geoculus_number")
    dendroculi: int = Field(alias="dendroculus_number")
    electroculi: int = Field(alias="electroculus_number")
    common_chests: int = Field(alias="common_chest_number")
    exquisite_chests: int = Field(alias="exquisite_chest_number")
    precious_chests: int = Field(alias="precious_chest_number")
    luxurious_chests: int = Field(alias="luxurious_chest_number")
    remarkable_chests: int = Field(alias="magic_chest_number")
    unlocked_waypoints: int = Field(alias="way_point_number")
    unlocked_domains: int = Field(alias="domain_number")


class Offering(APIModel):
    """Exploration offering."""

    name: str
    level: int
    icon: str = ""


class Exploration(APIModel):
    """Exploration data."""

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

    offerings: List[Offering]

    @property
    def explored(self) -> float:
        """The percentage explored."""
        return self.raw_explored / 10

    @validator("offerings", pre=True)
    def add_base_offering(
        cls, offerings: List[Any], values: Dict[str, Any]
    ) -> List[Any]:
        if values["type"] == "Reputation" and not any(
            values["type"] == o["name"] for o in offerings
        ):
            offerings = [*offerings, dict(name=values["type"], level=values["level"])]

        return offerings


class TeapotRealm(APIModel):
    """A specific teapot realm."""

    name: str
    icon: str

    @property
    def id(self) -> int:
        match = re.search(r"\d", self.icon)
        return int(match.group()) if match else 0


class Teapot(APIModel):
    """User's Serenitea Teapot."""

    realms: List[TeapotRealm]
    level: int
    visitors: int = Field(alias="visit_num")
    comfort: int = Field(alias="comfort_num")
    items: int = Field(alias="item_num")
    comfort_name: str = Field(alias="comfort_level_name")
    comfort_icon: str = Field(alias="comfort_level_icon")


class PartialGenshinUserStats(APIModel):
    """User stats with characters without equipment."""

    info: UserInfo = Field("role")
    stats: Stats
    characters: List[PartialCharacter] = Field(alias="avatars")
    explorations: List[Exploration] = Field(alias="world_explorations")
    teapot: Optional[Teapot] = Field(alias="homes")

    @validator("teapot", pre=True)
    def format_teapot(cls, v: Any) -> Optional[Dict[str, Any]]:
        if not v:
            return None
        if isinstance(v, dict):
            return cast("dict[str, Any]", v)
        return {**v[0], "realms": v}


class GenshinUserStats(PartialGenshinUserStats):
    """User stats with characters with equipment"""

    characters: List[Character] = Field(alias="avatars")


class FullGenshinUserStats(GenshinUserStats):
    """User stats with all data a user can have"""

    abyss: SpiralAbyssPair
    activities: Dict
