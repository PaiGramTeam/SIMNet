"""Starrail base character model."""
from simnet.models.base import APIModel


class StarRailBaseCharacter(APIModel):
    """Base character model."""

    id: int
    element: str
    rarity: int
    icon: str


class StarRailPartialCharacter(StarRailBaseCharacter):
    """Character without any equipment."""

    name: str
    level: int
    rank: int


class FloorCharacter(StarRailBaseCharacter):
    """Character in a floor."""

    level: int


class RogueCharacter(StarRailBaseCharacter):
    """Rogue character model."""

    level: int
    rank: int
    is_trial: bool = False


class ActivityCharacter(StarRailBaseCharacter):
    """Combat character model."""

    level: int
    is_trial: bool = False
