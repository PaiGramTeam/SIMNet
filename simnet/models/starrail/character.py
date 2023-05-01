from simnet.models.base import APIModel


class BaseCharacter(APIModel):
    """
    A class representing a character in a game.

    Attributes:
        id (:obj:`int`): The unique identifier of the character.
        name (:obj:`str`): The name of the character.
        element (:obj:`str`): The element that the character represents (e.g. fire, water, etc.).
        rarity (:obj:`int`): The rarity of the character (e.g. 1-5 stars).
    """

    id: int
    name: str
    element: str
    rarity: int
    icon: str
