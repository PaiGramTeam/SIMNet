import re
from typing import Dict, List, Optional

from simnet.models.base import APIModel, Field
from simnet.models.zzz.character import ZZZPartialCharacter


def desc_to_html(desc: str) -> str:
    output_text = re.sub(
        r"<color=(#[0-9a-fA-F]{6})>", r'<span style="color: \1">', desc
    )
    output_text = output_text.replace("</color>", "</span>")
    return output_text


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
    properties: List[ZZZCalculatorWeaponProperty]
    main_properties: List[ZZZCalculatorWeaponProperty]
    equip_suit: ZZZCalculatorEquipSuit
    equipment_type: int


class ZZZCalculatorCharacter(ZZZPartialCharacter):
    equip: List[ZZZCalculatorEquipment]
    weapon: Optional[ZZZCalculatorWeapon] = None
    properties: List[ZZZCalculatorAvatarProperty]
    skills: List[ZZZCalculatorAvatarSkill]
    ranks: List[ZZZCalculatorAvatarRank]

    @property
    def equip_map(self) -> Dict[str, Optional[ZZZCalculatorEquipment]]:
        data: Dict[str, Optional[ZZZCalculatorEquipment]] = {
            str(equip.equipment_type): equip for equip in self.equip
        }
        for i in range(1, 7):
            if str(i) not in data:
                data[str(i)] = None
        return data

    @property
    def equip_suits(self) -> List[ZZZCalculatorEquipSuit]:
        data = []
        for equip in self.equip:
            if equip.equip_suit in data:
                continue
            data.append(equip.equip_suit)
        data.sort(key=lambda x: x.own, reverse=True)
        return data


class ZZZCalculatorCharacterDetails(APIModel):
    characters: List[ZZZCalculatorCharacter] = Field(alias="avatar_list")
