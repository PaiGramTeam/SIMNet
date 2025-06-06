import re
from typing import Optional

from simnet.models.base import APIModel, Field
from simnet.models.zzz.character import ZZZPartialCharacter


def desc_to_html(desc: str) -> str:
    output_text = re.sub(r"<color=(#[0-9a-fA-F]{6})>", r'<span style="color: \1">', desc)
    return output_text.replace("</color>", "</span>")


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
    properties: list[ZZZCalculatorWeaponProperty]
    main_properties: list[ZZZCalculatorWeaponProperty]
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
    items: list[ZZZCalculatorAvatarSkillItem]

    @property
    def level_str(self) -> str:
        return str(self.level).zfill(2)


class ZZZCalculatorAvatarRank(APIModel):
    id: int
    name: str
    desc: str
    pos: int
    is_unlocked: bool


class ZZZCalculatorEquipSuit(APIModel):
    suit_id: int
    name: str
    own: int
    desc1: str
    desc2: str

    @property
    def desc1_html(self) -> str:
        return desc_to_html(self.desc1)

    @property
    def desc2_html(self) -> str:
        return desc_to_html(self.desc2)


class ZZZCalculatorEquipment(APIModel):
    id: int
    level: int
    name: str
    icon: str
    rarity: str
    properties: list[ZZZCalculatorWeaponProperty]
    main_properties: list[ZZZCalculatorWeaponProperty]
    equip_suit: ZZZCalculatorEquipSuit
    equipment_type: int


class ZZZCalculatorCharacter(ZZZPartialCharacter):
    equip: list[ZZZCalculatorEquipment]
    weapon: Optional[ZZZCalculatorWeapon] = None
    properties: list[ZZZCalculatorAvatarProperty]
    skills: list[ZZZCalculatorAvatarSkill]
    ranks: list[ZZZCalculatorAvatarRank]

    @property
    def equip_map(self) -> dict[str, Optional[ZZZCalculatorEquipment]]:
        data: dict[str, Optional[ZZZCalculatorEquipment]] = {str(equip.equipment_type): equip for equip in self.equip}
        for i in range(1, 7):
            if str(i) not in data:
                data[str(i)] = None
        return data

    @property
    def equip_suits(self) -> list[ZZZCalculatorEquipSuit]:
        data = []
        for equip in self.equip:
            if equip.equip_suit in data:
                continue
            data.append(equip.equip_suit)
        data.sort(key=lambda x: x.own, reverse=True)
        return data


class ZZZCalculatorCharacterDetails(APIModel):
    characters: list[ZZZCalculatorCharacter] = Field(alias="avatar_list")
