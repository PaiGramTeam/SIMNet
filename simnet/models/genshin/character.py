__all__ = ("BaseCharacter",)

from simnet.models.base import APIModel


class BaseCharacter(APIModel):
    """Base character model."""

    id: int
    name: str
    element: str
    rarity: int
    icon: str

    collab: bool = False

    @property
    def traveler_name(self) -> str:
        if self.id == 10000005:
            return "Aether"
        elif self.id == 10000007:
            return "Lumine"
        else:
            return ""
