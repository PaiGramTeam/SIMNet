"""Starrail chronicle character."""
from typing import List, Optional, Any, Dict

from pydantic import validator

from simnet.models.base import APIModel

from .. import character

__all__ = [
    "StarRailEquipment",
    "RelicProp",
    "Relic",
    "Rank",
    "CharacterProp",
    "SkillStage",
    "Skill",
    "StarRailDetailCharacter",
    "EquipWiki",
    "PropertyInfo",
    "RecommendProperty",
    "RelicProperty",
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

    @property
    def show_add(self) -> bool:
        """Show add."""
        return self.add not in ["0.0", "0.0%", "0"]


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

    @property
    def skills_map(self) -> List[List[Skill]]:
        """Map skills."""
        data = []
        for skill in filter(lambda x: x.point_type == 3, self.skills):
            data.append([skill])
        skills = list(filter(lambda x: x.point_type == 1 and x.pre_point, self.skills))
        for _ in range(10):
            for skill in skills.copy():
                for item in data:
                    item_ids = [i.point_id for i in item]
                    if skill.pre_point in item_ids and skill.point_id not in item_ids:
                        item.append(skill)
                        skills.remove(skill)
                        break
            if not skills:
                break
        new_data = []
        for item in data:
            new_data.append(sorted(item, key=lambda x: x.point_id))
        return new_data

    @property
    def skills_single(self) -> List[Skill]:
        """Single skills."""
        skills = list(filter(lambda x: x.point_type == 1, self.skills))
        map_ids = []
        for item in self.skills_map:
            map_ids.extend([i.point_id for i in item])
        return [i for i in skills if i.point_id not in map_ids]

    @property
    def skills_main(self) -> List[Skill]:
        """Main skills."""
        return self.skills[:4]


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
        if isinstance(v, list):
            return v
        new_list = []
        for k, value in v.items():
            if isinstance(value, str):
                v_ = {value_key: value}
            else:
                v_ = value
            if key:
                v_[key] = k
            new_list.append(v_)
        return new_list

    @validator("equip_wiki", pre=True)
    def parse_equip_wiki(cls, v: Dict[str, str]) -> List[Dict[str, str]]:
        """Parse equip wiki."""
        return cls._parse(v, "id", "url")

    @validator("property_info", pre=True)
    def parse_property_info(cls, v: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse property info."""
        return cls._parse(v)

    @validator("recommend_property", pre=True)
    def parse_recommend_property(cls, v: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse recommend property."""
        return cls._parse(v, "id")

    def get_recommend_property_by_cid(self, character_id: int) -> Optional[RecommendProperty]:
        """Get recommend property by character id."""
        for i in self.recommend_property:
            if i.id == character_id:
                return i
        return None
