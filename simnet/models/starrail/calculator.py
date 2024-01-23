"""Starrail calculator models."""
from typing import Dict, Any, Optional, List

from pydantic import Field, validator

from simnet.models.base import APIModel
from simnet.models.starrail.character import StarRailBaseCharacter, StarRailElement, StarRailDestiny

__all__ = (
    "CALCULATOR_ELEMENTS",
    "CALCULATOR_DESTINIES",
    "StarrailCalculatorCharacter",
    "StarrailCalculatorWeapon",
    "StarrailCalculatorSkill",
    "StarrailCalculatorCharacterDetails",
)
CALCULATOR_ELEMENTS: Dict[int, StarRailElement] = {
    1: StarRailElement.Physical,
    2: StarRailElement.Pyro,
    4: StarRailElement.Cryo,
    8: StarRailElement.Electro,
    16: StarRailElement.Anemo,
    32: StarRailElement.Quantum,
    64: StarRailElement.Nombre,
}
CALCULATOR_DESTINIES: Dict[int, StarRailDestiny] = {
    1: StarRailDestiny.HuiMie,
    2: StarRailDestiny.XunLie,
    3: StarRailDestiny.ZhiShi,
    4: StarRailDestiny.TongXie,
    5: StarRailDestiny.XuWu,
    6: StarRailDestiny.CunHu,
    7: StarRailDestiny.FengRao,
}


class StarrailCalculatorCharacter(StarRailBaseCharacter):
    """Character meant to be used with calculators.

    Attributes:
        id (int): The ID of the character.
        element (str): The element of the character.
        icon (str): The icon of the character.
        name (str): The name of the character.
        path (str): The path type of the character.
        max_level (int): The maximum level of the character.
        cur_level (int): The current level of the character.
        target_level (int): The target level of the character.
        is_forward (bool): Whether the character is forward.
    """

    id: int = Field(alias="item_id")
    element: StarRailElement = Field(alias="damage_type")
    icon: str = Field(alias="icon_url")

    name: str = Field(alias="item_name")
    path: StarRailDestiny = Field(alias="avatar_base_type")

    max_level: int
    cur_level: int
    target_level: int
    is_forward: bool

    @validator("element", pre=True)
    def parse_element(cls, v: Any) -> str:
        """Parse the element of a character.

        Args:
            v (Any): The value of the element.

        Returns:
            str: The parsed element.
        """
        if isinstance(v, str) and v.isnumeric():
            return CALCULATOR_ELEMENTS[int(v)].value
        return v

    @validator("path", pre=True)
    def parse_path(cls, v: Any) -> str:
        """Parse the path type of character.

        Args:
            v (Any): The value of the path type.

        Returns:
            str: The parsed path type.
        """
        if isinstance(v, str) and v.isnumeric():
            return CALCULATOR_DESTINIES[int(v)].value
        return v


class StarrailCalculatorWeapon(APIModel):
    """Weapon meant to be used with calculators.

    Attributes:
        id (int): The ID of the weapon.
        name (str): The name of the weapon.
        icon (str): The icon of the weapon.
        rarity (int): The rarity of the weapon.
        path (str): The path type of the weapon.
        max_level (int): The maximum level of the weapon.
        cur_level (int): The current level of the weapon.
        target_level (int): The target level of the weapon.
        is_forward (bool): Whether the weapon is forward.
    """

    id: int = Field(alias="item_id")
    name: str = Field(alias="item_name")
    icon: str = Field(alias="item_url")
    rarity: int
    path: StarRailDestiny = Field(alias="avatar_base_type")

    max_level: int
    cur_level: int
    target_level: int
    is_forward: bool

    @validator("path", pre=True)
    def parse_path(cls, v: Any) -> str:
        """Parse the path type of weapon.

        Args:
            v (Any): The value of the path type.

        Returns:
            str: The parsed path type.
        """
        if isinstance(v, str) and v.isnumeric():
            return CALCULATOR_DESTINIES[int(v)].value
        return v


class StarrailCalculatorSkill(APIModel):
    """Talent of a character meant to be used with calculators.

    Attributes:
        id (int): The ID of the talent.
        pre_point (int): The previous point of the talent.
        point_type (int): The type of the talent.
        anchor (str): The anchor of the talent.
        icon (str): The icon of the talent.
        max_level (int): The maximum level of the talent.
        cur_level (int): The current level of the talent.
        target_level (int): The target level of the talent.
        progress (str): The progress of the talent.
        min_level_limit (int): The minimum level limit of the talent.
    """

    id: int = Field(alias="point_id")
    pre_point: int
    point_type: int
    anchor: str
    icon: str = Field(alias="item_url")

    max_level: int
    cur_level: int
    target_level: int
    progress: str
    min_level_limit: int

    @property
    def learned(self) -> bool:
        return self.progress == "Learned"


class StarrailCalculatorCharacterDetails(APIModel):
    """Details of a synced calculator

    Attributes:
        avatar (StarrailCalculatorCharacter): The character of the calculator.
        equipment (Optional[StarrailCalculatorWeapon]): The weapon of the calculator.
        skills (List[StarrailCalculatorSkill]): The skills of the calculator.
        skills_other (List[StarrailCalculatorSkill]): The other skills of the calculator.
    """

    avatar: StarrailCalculatorCharacter
    equipment: Optional[StarrailCalculatorWeapon] = None
    skills: List[StarrailCalculatorSkill]
    skills_other: List[StarrailCalculatorSkill]
