"""Starrail chronicle character."""
from typing import List, Optional, Any, Dict

from pydantic import validator

from simnet.models.base import APIModel

from .. import character

__all__ = [
    "StarRailEquipment",
    "Rank",
    "Relic",
    "StarRailDetailCharacter",
    "StarRailDetailCharacters",
]


class StarRailEquipment(APIModel):
    """Character equipment."""

    id: int
    level: int
    rank: int
    name: str
    desc: str
    icon: str


class RelicProp(APIModel):
    """Character relic property."""

    property_type: int
    times: int
    value: str


class Relic(APIModel):
    """Character relic."""

    id: int
    level: int
    pos: int
    name: str
    desc: str
    icon: str
    rarity: int
    main_property: RelicProp
    properties: List[RelicProp]


class Rank(APIModel):
    """Character rank."""

    id: int
    pos: int
    name: str
    icon: str
    desc: str
    is_unlocked: bool


class CharacterProp(APIModel):
    """Character property."""

    property_type: int
    base: str
    add: str
    final: str


class SkillStage(APIModel):
    """Character skill stage."""

    desc: str
    name: str
    level: int
    remake: str
    item_url: str
    is_activated: bool
    is_rank_work: bool


class Skill(APIModel):
    """Character skill."""

    point_id: int
    point_type: int
    item_url: str
    level: int
    is_activated: bool
    is_rank_work: bool
    pre_point: int
    anchor: str
    remake: str
    skill_stages: List[SkillStage]


class StarRailDetailCharacter(character.StarRailPartialCharacter):
    """StarRail character with equipment and relics."""

    image: str
    equip: Optional[StarRailEquipment]
    relics: List[Relic]
    ornaments: List[Relic]
    ranks: List[Rank]
    properties: List[CharacterProp]
    skills: List[Skill]
    base_type: int
    figure_path: str


class EquipWiki(APIModel):
    """Equipment wiki."""

    id: int
    url: str


class PropertyInfo(APIModel):
    """Property info."""

    property_type: int
    name: str
    icon: str
    property_name_relic: str
    property_name_filter: str


class RecommendProperty(APIModel):
    """Recommend property."""

    id: int
    recommend_relic_properties: List[int]
    custom_relic_properties: List[int]
    is_custom_property_valid: bool


class RelicProperty(APIModel):
    """Relic property."""

    property_type: int
    modify_property_type: int


class StarRailDetailCharacters(APIModel):
    """StarRail characters."""

    avatar_list: List[StarRailDetailCharacter]
    equip_wiki: List[EquipWiki]
    property_info: List[PropertyInfo]
    recommend_property: List[RecommendProperty]
    relic_properties: List[RelicProperty]

    @staticmethod
    def _parse(v: Dict[str, Any], key: str = None, value_key: str = None) -> List[Dict[str, Any]]:
        """Parse dict to list."""
        new_list = []
        for k, v in v.items():
            if isinstance(v, str):
                v = {value_key: v}
            if key:
                v[key] = k
            new_list.append(v)
        return new_list

    @validator("equip_wiki", pre=True)
    def parse_equip_wiki(cls, v: Dict[str, str]) -> List[Dict[str, str]]:
        """Parse equip wiki."""
        return cls._parse(v, "id", "url")

    @validator("property_info", pre=True)
    def parse_property_info(cls, v: Dict[str, str]) -> List[Dict[str, str]]:
        """Parse property info."""
        return cls._parse(v)

    @validator("recommend_property", pre=True)
    def parse_recommend_property(cls, v: Dict[str, str]) -> List[Dict[str, str]]:
        """Parse recommend property."""
        return cls._parse(v, "id")
