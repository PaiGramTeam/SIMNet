"""Genshin calculator models."""
import collections
from typing import Dict, Any, Literal, Optional, List

from pydantic import Field, validator

from simnet.models.base import APIModel
from simnet.models.genshin.character import BaseCharacter

__all__ = (
    "CALCULATOR_ARTIFACTS",
    "CALCULATOR_ELEMENTS",
    "CALCULATOR_WEAPON_TYPES",
    "CalculatorArtifact",
    "CalculatorArtifactResult",
    "CalculatorCharacter",
    "CalculatorCharacterDetails",
    "CalculatorConsumable",
    "CalculatorFurnishing",
    "CalculatorFurnishingResults",
    "CalculatorResult",
    "CalculatorTalent",
    "CalculatorWeapon",
)
CALCULATOR_ELEMENTS: Dict[int, str] = {
    1: "Pyro",
    2: "Anemo",
    3: "Geo",
    4: "Dendro",
    5: "Electro",
    6: "Hydro",
    7: "Cryo",
}
CALCULATOR_WEAPON_TYPES: Dict[int, str] = {
    1: "Sword",
    10: "Catalyst",
    11: "Claymore",
    12: "Bow",
    13: "Polearm",
}
CALCULATOR_ARTIFACTS: Dict[int, str] = {
    1: "Flower of Life",
    2: "Plume of Death",
    3: "Sands of Eon",
    4: "Goblet of Eonothem",
    5: "Circlet of Logos",
}


class CalculatorCharacter(BaseCharacter):
    """Character meant to be used with calculators.

    Attributes:
        rarity (int): The rarity of the character.
        element (str): The element of the character.
        weapon_type (str): The type of weapon used by the character.
        level (int): The current level of the character.
        max_level (int): The maximum level of the character.
    """

    rarity: int = Field(alias="avatar_level")
    element: str = Field(alias="element_attr_id")
    weapon_type: str = Field(alias="weapon_cat_id")
    level: int = Field(alias="level_current", default=0)
    max_level: int

    @validator("element", pre=True)
    def parse_element(cls, v: Any) -> str:
        """Parse the element of a character.

        Args:
            v (Any): The value of the element.

        Returns:
            str: The parsed element.
        """
        if isinstance(v, str):
            return v

        return CALCULATOR_ELEMENTS[int(v)]

    @validator("weapon_type", pre=True)
    def parse_weapon_type(cls, v: Any) -> str:
        """Parse the weapon type of character.

        Args:
            v (Any): The value of the weapon type.

        Returns:
            str: The parsed weapon type.
        """
        if isinstance(v, str):
            return v

        return CALCULATOR_WEAPON_TYPES[int(v)]


class CalculatorWeapon(APIModel):
    """Weapon meant to be used with calculators.

    Attributes:
        id (int): The ID of the weapon.
        name (str): The name of the weapon.
        icon (str): The icon of the weapon.
        rarity (int): The rarity of the weapon.
        type (str): The type of weapon.
        level (int): The current level of the weapon.
        max_level (int): The maximum level of the weapon.
    """

    id: int
    name: str
    icon: str
    rarity: int = Field(alias="weapon_level")
    type: str = Field(alias="weapon_cat_id")
    level: int = Field(alias="level_current", default=0)
    max_level: int

    @validator("type", pre=True)
    def parse_weapon_type(cls, v: Any) -> str:
        """
        Parse the type of weapon.

        Args:
            v (Any): The value of the weapon type.

        Returns:
            str: The parsed weapon type.
        """
        if isinstance(v, str):
            return v

        return CALCULATOR_WEAPON_TYPES[int(v)]


class CalculatorArtifact(APIModel):
    """Artifact meant to be used with calculators.

    Attributes:
        id (int): The ID of the artifact.
        name (str): The name of the artifact.
        icon (str): The icon of the artifact.
        rarity (int): The rarity of the artifact.
        pos (int): The position of the artifact.
        level (int): The current level of the artifact.
        max_level (int): The maximum level of the artifact.
    """

    id: int
    name: str
    icon: str
    rarity: int = Field(alias="reliquary_level")
    pos: int = Field(alias="reliquary_cat_id")
    level: int = Field(alias="level_current", default=0)
    max_level: int

    @property
    def pos_name(self) -> str:
        """The name of the artifact position.

        Returns:
            str: The name of the artifact position.
        """
        return CALCULATOR_ARTIFACTS[self.pos]


class CalculatorTalent(APIModel):
    """Talent of a character meant to be used with calculators.

    Attributes:
        id (int): The ID of the talent.
        group_id (int): The group ID of the talent.
        name (str): The name of the talent.
        icon (str): The icon of the talent.
        level (int): The current level of the talent.
        max_level (int): The maximum level of the talent.
    """

    id: int
    group_id: int  # proudSkillGroupId
    name: str
    icon: str
    level: int = Field(alias="level_current", default=0)
    max_level: int

    @property
    def type(self) -> Optional[Literal["attack", "skill", "burst", "passive", "dash"]]:
        """The type of the talent, parsed from the group ID.

        Returns:
            Optional[Literal["attack", "skill", "burst", "passive", "dash"]]: The type of the talent.
                Returns `None` if the type cannot be determined.
        """
        # special cases
        if self.id == self.group_id:
            return "passive"  # maybe hoyo does this for upgradable?

        if len(str(self.id)) == 6:  # in candSkillDepotIds
            return "attack"

        # 4139 -> group=41 identifier=3 order=9
        _, relevant = divmod(self.group_id, 100)
        identifier, order = divmod(relevant, 10)

        if identifier == 2:
            return "passive"
        if order == 1:
            return "attack"
        if order == 2:
            return "skill"
        if order == 9:
            return "burst"
        if order == 3:
            return "dash"
        return None

    @property
    def upgradeable(self) -> bool:
        """Whether this talent can be leveled up.

        Returns:
            bool: Whether this talent can be leveled up.
        """
        return self.type not in ("passive", "dash")


class CalculatorFurnishing(APIModel):
    """Furnishing meant to be used with calculators.

    Attributes:
        id (int): The ID of the furnishing.
        name (str): The name of the furnishing.
        icon (str): The icon URL of the furnishing.
        rarity (int): The rarity level of the furnishing.
        amount (int, optional): The amount of the furnishing, if applicable.
    """

    id: int
    name: str
    icon: str = Field(alias="icon_url")
    rarity: int = Field(alias="level")

    amount: Optional[int] = Field(alias="num")


class CalculatorCharacterDetails(APIModel):
    """Details of a synced calculator

    Attributes:
        weapon (CalculatorWeapon, optional): The calculator weapon.
        talents (List[CalculatorTalent]): A list of calculator talents.
        artifacts (List[CalculatorArtifact]): A list of calculator artifacts.
    """

    weapon: Optional[CalculatorWeapon] = Field(alias="weapon")
    talents: List[CalculatorTalent] = Field(alias="skill_list")
    artifacts: List[CalculatorArtifact] = Field(alias="reliquary_list")

    @validator("talents")
    def correct_talent_current_level(cls, v: List[CalculatorTalent]) -> List[CalculatorTalent]:
        """Validates the current level of each calculator talent in the talents list and sets it to 1 if it is 0.

        Args:
            cls: The class.
            v (List[CalculatorTalent]): The list of calculator talents to validate.

        Returns:
            List[CalculatorTalent]: The list of validated calculator talents.
        """
        # passive talent have current levels at 0 for some reason
        talents: List[CalculatorTalent] = []

        for talent in v:
            if talent.max_level == 1 and talent.level == 0:
                raw = talent.dict()
                raw["level"] = 1
                talent = CalculatorTalent(**raw)

            talents.append(talent)

        return v

    @property
    def upgradeable_talents(self) -> List[CalculatorTalent]:
        """Returns a list of all calculator talents that can be leveled up.

        Returns:
            List[CalculatorTalent]: A list of all calculator talents that can be leveled up.
        """
        if self.talents[2].type == "dash":
            return [self.talents[0], self.talents[1], self.talents[3]]
        return [self.talents[0], self.talents[1], self.talents[2]]


class CalculatorConsumable(APIModel):
    """Item consumed when upgrading.

    Attributes:
        id (int): The ID of the consumable.
        name (str): The name of the consumable.
        icon (str): The URL of the icon of the consumable.
        amount (int): The number of this consumable used.
    """

    id: int
    name: str
    icon: str
    amount: int = Field(alias="num")


class CalculatorArtifactResult(APIModel):
    """Calculation result for a specific artifact.

    Attributes:
        artifact_id (int): The ID of the artifact.
        consumable_list (List[CalculatorConsumable]): A list of CalculatorConsumable objects representing the
            consumables used by this artifact.
    """

    artifact_id: int = Field(alias="reliquary_id")
    consumable_list: List[CalculatorConsumable] = Field(alias="id_consume_list")


class CalculatorResult(APIModel):
    """
    Calculation result.

    Attributes:
        character (List[CalculatorConsumable]): Consumables used by characters.
        weapon (List[CalculatorConsumable]): Consumables used by weapons.
        talents (List[CalculatorConsumable]): Consumables used by talents.
        artifacts (List[CalculatorArtifactResult]): Artifacts used.
    """

    character: List[CalculatorConsumable] = Field(alias="avatar_consume")
    weapon: List[CalculatorConsumable] = Field(alias="weapon_consume")
    talents: List[CalculatorConsumable] = Field(alias="avatar_skill_consume")
    artifacts: List[CalculatorArtifactResult] = Field(alias="reliquary_consume")

    @property
    def total(self) -> List[CalculatorConsumable]:
        """Returns the total consumables used across all categories.

        Returns:
            List[CalculatorConsumable]: A list of CalculatorConsumable objects representing the total
            consumables used across all categories.
        """
        artifacts = [i for a in self.artifacts for i in a.consumable_list]  # skipcq: PYL-E1133
        combined = self.character + self.weapon + self.talents + artifacts

        grouped: Dict[int, List[CalculatorConsumable]] = collections.defaultdict(list)
        for i in combined:
            grouped[i.id].append(i)

        total = [
            CalculatorConsumable(
                id=x[0].id,
                name=x[0].name,
                icon=x[0].icon,
                num=sum(i.amount for i in x),
            )
            for x in grouped.values()
        ]

        return total


class CalculatorFurnishingResults(APIModel):
    """Furnishing calculation result.

    Attributes:
        furnishings (List[CalculatorConsumable]): A list of CalculatorConsumable objects representing the
            furnishings used.
    """

    furnishings: List[CalculatorConsumable] = Field(alias="list")

    @property
    def total(self) -> List[CalculatorConsumable]:
        """Returns the total furnishings used.

        Returns:
            List[CalculatorConsumable]: A list of CalculatorConsumable objects representing the total
            furnishings used.
        """
        return self.furnishings
