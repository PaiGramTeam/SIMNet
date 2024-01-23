"""Starrail base character model."""
from enum import Enum

from simnet.models.base import APIModel


class StarRailDestiny(str, Enum):
    """命途"""

    HuiMie = "毁灭"
    ZhiShi = "智识"
    XunLie = "巡猎"
    CunHu = "存护"
    FengRao = "丰饶"
    TongXie = "同谐"
    XuWu = "虚无"


class StarRailElement(str, Enum):
    """属性"""

    Physical = "物理"
    Pyro = "火"
    Anemo = "风"
    Electro = "雷"
    Cryo = "冰"
    Nombre = "虚数"
    Quantum = "量子"
    Null = "NULL"
    """无"""


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


class RogueCharacter(StarRailBaseCharacter):
    """Rogue character model."""

    level: int
    rank: int
    is_trial: bool = False


class ActivityCharacter(StarRailBaseCharacter):
    """Combat character model."""

    level: int
    is_trial: bool = False
