from typing import Optional

from simnet.models.base import APIModel

__all__ = ("BaseCharacter",)


class BaseCharacter(APIModel):
    """A base class for all Genshin Impact characters.

    Attributes:
        id (int): The unique identifier of the character.
        name (str): The name of the character.
        element (str): The elemental affinity of the character.
        rarity (int): The rarity level of the character.
        icon (str): The URL of the icon image for the character.

        collab (bool, optional): Whether the character is a collaboration character. Defaults to False.

    Properties:
        traveler_name (str): If the character ID matches the traveler's ID, returns the name of the traveler character.
    """

    id: int
    name: Optional[str] = None
    element: Optional[str] = None
    rarity: Optional[int] = None
    icon: Optional[str] = None

    collab: bool = False

    @property
    def traveler_name(self) -> str:
        """If the character ID matches the traveler's ID, returns the name of the traveler character.

        Returns:
            str: The name of the traveler character if the ID matches, otherwise an empty string.
        """
        if self.id == 10000005:
            return "Aether"
        if self.id == 10000007:
            return "Lumine"
        return ""
