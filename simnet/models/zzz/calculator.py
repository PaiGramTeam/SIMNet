from typing import List

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.zzz.character import ZZZPartialCharacter


class ZZZCalculatorWeaponProperty(APIModel):

    property_name: str
    property_id: int
    base: str


class ZZZCalculatorWeapon(APIModel):

    id: int
    level: int
    name: str
    star: int
    icon: str
    rarity: str
    properties: List[ZZZCalculatorWeaponProperty]
    main_properties: List[ZZZCalculatorWeaponProperty]
    talent_title: str
    talent_content: str
    profession: int


class ZZZCalculatorAvatarProperty(ZZZCalculatorWeaponProperty):

    add: str
    final: str


class ZZZCalculatorAvatarSkillItem(APIModel):
    title: str
    text: str


class ZZZCalculatorAvatarSkill(APIModel):

    level: int
    skill_type: int
    items: List[ZZZCalculatorAvatarSkillItem]


class ZZZCalculatorAvatarRank(APIModel):

    id: int
    name: str
    desc: str
    pos: int
    is_unlocked: bool


class ZZZCalculatorCharacter(ZZZPartialCharacter):

    equip: List
    weapon: ZZZCalculatorWeapon
    properties: List[ZZZCalculatorAvatarProperty]
    skills: List[ZZZCalculatorAvatarSkill]
    ranks: List[ZZZCalculatorAvatarRank]


class ZZZCalculatorCharacterDetails(APIModel):

    characters: List[ZZZCalculatorCharacter] = Field(alias="avatar_list")
