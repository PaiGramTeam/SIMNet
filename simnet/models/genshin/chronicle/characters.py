from typing import List, Dict

from pydantic import Field, validator

from simnet.models.base import APIModel
from simnet.models.genshin.character import BaseCharacter

__all__ = (
    "Artifact",
    "ArtifactSet",
    "ArtifactSetEffect",
    "Character",
    "CharacterWeapon",
    "Constellation",
    "Outfit",
    "PartialCharacter",
)


class PartialCharacter(BaseCharacter):
    """
    Represents a Genshin Impact character without any equipment.

    Attributes:
        level (int): The character's level.
        friendship (int): The character's friendship level (also known as fetter).
        constellation (int): The number of constellations that are currently active for the character.
    """

    icon: str = Field(alias="image")
    level: int
    friendship: int = Field(alias="fetter")
    constellation: int = Field(alias="actived_constellation_num")


class CharacterWeapon(APIModel):
    """
    Represents a character's equipped weapon.

    Attributes:
        id (int): The weapon's ID number.
        icon (str): The URL of the weapon's icon.
        name (str): The name of the weapon.
        rarity (int): The rarity (number of stars) of the weapon.
        description (str): The description of the weapon.
        level (int): The level of the weapon.
        type (str): The type of the weapon (e.g. Sword, Bow, etc.).
        ascension (int): The ascension level of the weapon.
        refinement (int): The refinement level of the weapon.
    """

    id: int
    icon: str
    name: str
    rarity: int
    description: str = Field(alias="desc")
    level: int
    type: str = Field(alias="type_name")
    ascension: int = Field(alias="promote_level")
    refinement: int = Field(alias="affix_level")


class ArtifactSetEffect(APIModel):
    """
    Represents the effect of an artifact set.

    Attributes:
        pieces (int): The number of artifact pieces required to activate the effect.
        effect (str): The description of the effect.
        enabled (bool): Whether the effect is currently enabled for the character's equipped artifacts.
            Defaults to False.
    """

    pieces: int = Field(alias="activation_number")
    effect: str
    enabled: bool = False


class ArtifactSet(APIModel):
    """
    Represents an artifact set.

    Attributes:
        id (int): The artifact set's ID number.
        name (str): The name of the artifact set.
        effects (List[ArtifactSetEffect]): The effects of the artifact set.
    """

    id: int
    name: str
    effects: List[ArtifactSetEffect] = Field(alias="affixes")


class Artifact(APIModel):
    """
    Represents a character's equipped artifact.

    Attributes:
        id (int): The artifact's ID number.
        icon (str): The URL of the artifact's icon.
        name (str): The name of the artifact.
        pos_name (str): The name of the artifact's position (e.g. Flower of Life, Plume of Death, etc.).
        pos (int): The position of the artifact (1-5).
        rarity (int): The rarity (number of stars) of the artifact.
        level (int): The level of the artifact.
        set (ArtifactSet): The artifact set that the artifact belongs to.
    """

    id: int
    icon: str
    name: str
    pos_name: str
    pos: int
    rarity: int
    level: int
    set: ArtifactSet


class Constellation(APIModel):
    """
    Represents a character constellation.

    Attributes:
        id (int): The ID number of the constellation.
        icon (str): The URL of the constellation's icon.
        pos (int): The position of the constellation (1-6).
        name (str): The name of the constellation.
        effect (str): The description of the effect.
        activated (bool): Whether the constellation is currently activated. Defaults to False.
    """

    id: int
    icon: str
    pos: int
    name: str
    effect: str
    activated: bool = Field(alias="is_actived")

    @property
    def scaling(self) -> bool:
        """Returns whether the constellation is simply for talent scaling."""
        return "U" in self.icon


class Outfit(APIModel):
    """
    Represents an outfit of a character.

    Attributes:
        id (int): The ID number of the outfit.
        icon (str): The URL of the outfit's icon.
        name (str): The name of the outfit.
    """

    id: int
    icon: str
    name: str


class Character(PartialCharacter):
    """
    Represents a Genshin Impact character with equipment.

    Attributes:
        weapon (CharacterWeapon): The character's equipped weapon.
        artifacts (List[Artifact]): The character's equipped artifacts.
        constellations (List[Constellation]): The character's constellations.
        outfits (List[Outfit]): The character's outfits.
    """

    weapon: CharacterWeapon
    artifacts: List[Artifact] = Field(alias="reliquaries")
    constellations: List[Constellation]
    outfits: List[Outfit] = Field(alias="costumes")

    @validator("artifacts")
    def add_artifact_effect_enabled(cls, artifacts: List[Artifact]) -> List[Artifact]:
        """
        Determines which artifact set effects are enabled for the character's equipped artifacts.

        Args:
            artifacts (List[Artifact]): The character's equipped artifacts.

        Returns:
            List[Artifact]: The character's equipped artifacts with their corresponding artifact set effects enabled if
          applicable.
        """
        sets: Dict[int, List[Artifact]] = {}
        for arti in artifacts:
            sets.setdefault(arti.set.id, []).append(arti)

        for artifact in artifacts:
            for effect in artifact.set.effects:
                if effect.pieces <= len(sets[artifact.set.id]):
                    effect.enabled = True

        return artifacts
