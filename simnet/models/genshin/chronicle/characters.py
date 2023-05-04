from typing import List, Dict

import pydantic


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

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.genshin.character import BaseCharacter


class PartialCharacter(BaseCharacter):
    """Character without any equipment."""

    level: int
    friendship: int = Field(alias="fetter")
    constellation: int = Field(alias="actived_constellation_num")


class CharacterWeapon(APIModel):
    """Character's equipped weapon."""

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
    """Effect of an artifact set."""

    pieces: int = Field(alias="activation_number")
    effect: str
    enabled: bool = False


class ArtifactSet(APIModel):
    """Artifact set."""

    id: int
    name: str
    effects: List[ArtifactSetEffect] = Field(alias="affixes")


class Artifact(APIModel):
    """Character's equipped artifact."""

    id: int
    icon: str
    name: str
    pos_name: str
    pos: int
    rarity: int
    level: int
    set: ArtifactSet


class Constellation(APIModel):
    """Character constellation."""

    id: int
    icon: str
    pos: int
    name: str
    effect: str
    activated: bool = Field(alias="is_actived")

    @property
    def scaling(self) -> bool:
        """Whether the constellation is simply for talent scaling"""
        return "U" in self.icon


class Outfit(APIModel):
    """Outfit of a character."""

    id: int
    icon: str
    name: str


class Character(PartialCharacter):
    """Character with equipment."""

    weapon: CharacterWeapon
    artifacts: List[Artifact] = Field(alias="reliquaries")
    constellations: List[Constellation]
    outfits: List[Outfit] = Field(alias="costumes")

    @pydantic.validator("artifacts")
    def add_artifact_effect_enabled(cls, artifacts: List[Artifact]) -> List[Artifact]:
        sets: Dict[int, List[Artifact]] = {}
        for arti in artifacts:
            sets.setdefault(arti.set.id, []).append(arti)

        for artifact in artifacts:
            for effect in artifact.set.effects:
                if effect.pieces <= len(sets[artifact.set.id]):
                    effect.enabled = True

        return artifacts
