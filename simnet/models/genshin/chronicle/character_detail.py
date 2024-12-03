import enum
import typing

from pydantic import field_validator

from simnet.models.base import APIModel, Field
from simnet.models.genshin.chronicle.characters import (
    Artifact,
    CharacterWeapon,
    Constellation,
    Outfit,
    PartialCharacter,
)


class GenshinWeaponType(enum.IntEnum):
    """Character weapon types."""

    SWORD = 1
    CATALYST = 10
    CLAYMORE = 11
    BOW = 12
    POLEARM = 13


class GenshinCharacterListInfoWeapon(APIModel):
    """A class representing information about a Genshin Impact character's weapon."""

    id: int
    icon: str
    type: GenshinWeaponType
    rarity: int
    level: int
    affix_level: int


class GenshinCharacterListInfo(PartialCharacter):
    """A class representing detailed information about a Genshin Impact character."""

    icon: str
    image: str
    side_icon: str

    weapon_type: GenshinWeaponType
    weapon: GenshinCharacterListInfoWeapon


class PropInfo(APIModel):
    """A property such as Crit Rate, HP, HP%."""

    type: int = Field(alias="property_type")
    name: str
    icon: typing.Optional[str] = None
    filter_name: str

    @field_validator("name", "filter_name")
    @classmethod
    def __fix_names(cls, value: str) -> str:  # skipcq: PTC-W0038
        r"""Fix "\xa0" in Crit Damage + Crit Rate names."""
        return value.replace("\xa0", " ")


class PropertyValue(APIModel):
    """A property with a value."""

    property_type: int
    base: str
    add: str
    final: str


class DetailCharacterWeapon(CharacterWeapon):
    """Detailed Genshin Weapon with main/sub stats."""

    type_int: GenshinWeaponType = Field(alias="type")

    main_property: PropertyValue
    sub_property: typing.Optional[PropertyValue] = None


class ArtifactProperty(APIModel):
    """Artifact's Property value & roll count."""

    property_type: int
    value: str
    times: int


class DetailArtifact(Artifact):
    """Detailed artifact with main/sub stats."""

    main_property: ArtifactProperty
    sub_property_list: typing.Sequence[ArtifactProperty]


class SkillAffix(APIModel):
    """Skill affix texts."""

    name: str
    value: str


class CharacterSkill(APIModel):
    """Character's skill."""

    id: int = Field(alias="skill_id")
    skill_type: int
    name: str
    level: int

    description: str = Field(alias="desc")
    affixes: typing.Sequence[SkillAffix] = Field(alias="skill_affix_list")
    icon: str
    is_unlocked: bool = Field(alias="is_unlock")


class GenshinDetailCharacter(APIModel):
    """Full Detailed Genshin Character"""

    base: GenshinCharacterListInfo
    weapon: DetailCharacterWeapon
    artifacts: typing.Sequence[DetailArtifact] = Field(alias="relics")

    constellations: typing.Sequence[Constellation]
    costumes: typing.Sequence[Outfit]

    skills: typing.Sequence[CharacterSkill]

    selected_properties: typing.Sequence[PropertyValue]
    base_properties: typing.Sequence[PropertyValue]
    extra_properties: typing.Sequence[PropertyValue]
    element_properties: typing.Sequence[PropertyValue]


class GenshinDetailCharacters(APIModel):
    """Genshin character list."""

    characters: typing.Sequence[GenshinDetailCharacter] = Field(alias="list")

    property_map: typing.Mapping[str, PropInfo]
    relic_property_options: typing.Mapping[str, typing.Sequence[int]]
