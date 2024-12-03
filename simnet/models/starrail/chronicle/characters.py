"""Starrail chronicle character."""

from typing import Any, Optional

from pydantic import field_validator

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
    properties: list[RelicProp]


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
    skill_stages: list[SkillStage]


class StarRailDetailCharacter(character.StarRailPartialCharacter):
    """StarRail character with equipment and relics."""

    image: str
    equip: Optional[StarRailEquipment] = None
    relics: list[Relic]
    ornaments: list[Relic]
    ranks: list[Rank]
    properties: list[CharacterProp]
    skills: list[Skill]
    base_type: int
    figure_path: str

    @property
    def skills_map(self) -> list[list[Skill]]:
        """Map skills."""
        data = [[skill] for skill in filter(lambda x: x.point_type == 3, self.skills)]
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
        return [sorted(item, key=lambda x: x.point_id) for item in data]

    @property
    def skills_single(self) -> list[Skill]:
        """Single skills."""
        skills = list(filter(lambda x: x.point_type == 1, self.skills))
        map_ids = []
        for item in self.skills_map:
            map_ids.extend([i.point_id for i in item])
        return [i for i in skills if i.point_id not in map_ids]

    @property
    def skills_main(self) -> list[Skill]:
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
    recommend_relic_properties: list[int]
    custom_relic_properties: list[int]
    is_custom_property_valid: bool


class RelicProperty(APIModel):
    """Relic property."""

    property_type: int
    modify_property_type: int


class StarRailDetailCharacters(APIModel):
    """StarRail characters."""

    avatar_list: list[StarRailDetailCharacter]
    equip_wiki: list[EquipWiki]
    property_info: list[PropertyInfo]
    recommend_property: list[RecommendProperty]
    relic_properties: list[RelicProperty]

    @staticmethod
    def _parse(v: dict[str, Any], key: str = None, value_key: str = None) -> list[dict[str, Any]]:
        """Parse dict to list."""
        if isinstance(v, list):
            return v
        new_list = []
        for k, value in v.items():
            v_ = {value_key: value} if isinstance(value, str) else value
            if key:
                v_[key] = k
            new_list.append(v_)
        return new_list

    @field_validator("equip_wiki", mode="before")
    @classmethod
    def parse_equip_wiki(cls, v: dict[str, str]) -> list[dict[str, str]]:
        """Parse equip wiki."""
        return cls._parse(v, "id", "url")

    @field_validator("property_info", mode="before")
    @classmethod
    def parse_property_info(cls, v: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse property info."""
        return cls._parse(v)

    @field_validator("recommend_property", mode="before")
    @classmethod
    def parse_recommend_property(cls, v: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse recommend property."""
        return cls._parse(v, "id")

    def get_recommend_property_by_cid(self, character_id: int) -> Optional[RecommendProperty]:
        """Get recommend property by character id."""
        for i in self.recommend_property:
            if i.id == character_id:
                return i
        return None
