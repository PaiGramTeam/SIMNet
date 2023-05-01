from typing import Optional, List

from simnet.models.base import APIModel
from simnet.models.starrail.character import BaseCharacter


class PartialCharacter(BaseCharacter):
    """A character without any equipment.

    Attributes:
        level (int): The level of the character.
        rank (int): The rank of the character.
    """

    level: int
    rank: int


class Equipment(APIModel):
    """An equipment model used in StarRailDetailCharacter.

    Attributes:
        id (int): The ID of the equipment.
        level (int): The level of the equipment.
        rank (int): The rank of the equipment.
        name (str): The name of the equipment.
        desc (str): The description of the equipment.
        icon (str): The icon of the equipment.
    """

    id: int
    level: int
    rank: int
    name: str
    desc: str
    icon: str


class Relic(APIModel):
    """A relic model used in StarRailDetailCharacter.

    Attributes:
        id (int): The ID of the relic.
        level (int): The level of the relic.
        pos (int): The position of the relic.
        name (str): The name of the relic.
        desc (str): The description of the relic.
        icon (str): The icon of the relic.
        rarity (int): The rarity of the relic.
    """

    id: int
    level: int
    pos: int
    name: str
    desc: str
    icon: str
    rarity: int


class Rank(APIModel):
    """A rank model used in StarRailDetailCharacter.

    Attributes:
        id (int): The ID of the rank.
        pos (int): The position of the rank.
        name (str): The name of the rank.
        icon (str): The icon of the rank.
        desc (str): The description of the rank.
        is_unlocked (bool): Whether the rank is unlocked.
    """

    id: int
    pos: int
    name: str
    icon: str
    desc: str
    is_unlocked: bool


class StarRailDetailCharacter(PartialCharacter):
    """A detailed character model used in StarShipDetailCharacters.

    Attributes:
        image (str): The image of the character.
        equip (Optional[Equipment]): The equipment of the character, if any.
        relics (List[Relic]): The relics of the character.
        ornaments (List[Relic]): The ornaments of the character.
        ranks (List[Rank]): The ranks of the character.
    """

    image: str
    equip: Optional[Equipment]
    relics: List[Relic]
    ornaments: List[Relic]
    ranks: List[Rank]


class StarShipDetailCharacters(APIModel):
    """A model containing a list of detailed characters used in the StarShipDetail API.

    Attributes:
        avatar_list (List[StarRailDetailCharacter]): The list of detailed characters.
    """

    avatar_list: List[StarRailDetailCharacter]
