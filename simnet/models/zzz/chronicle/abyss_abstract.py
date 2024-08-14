import datetime
from typing import List

from simnet.models.base import APIModel


class ZZZAbyssLevel(APIModel):
    """
    A data model representing an abyss level for ZZZ.

    Args:
        cur_level (int): The current abyss level.
        max_level: The maximum abyss level.
    """

    cur_level: int
    max_level: int
    icon: str


class ZZZAbyssPoint(APIModel):
    """
    A data model representing an abyss point.

    Args:
        cur_point (int): The current abyss point.
        max_point: The maximum abyss point.
    """

    cur_point: int
    max_point: int


class ZZZAbyssDuty(APIModel):
    """
    A data model representing an abyss duty for ZZZ.

    Args:
        cur_duty (int): The current abyss duty.
        max_duty: The maximum abyss duty.
    """

    cur_duty: int
    max_duty: int


class ZZZAbyssTalent(APIModel):
    """
    A data model representing abyss talent for ZZZ.

    Args:
        cur_talent (int): The current abyss talent.
        max_talent (int): The maximum abyss talent.
    """

    cur_talent: int
    max_talent: int


class ZZZAbyssCollectItem(APIModel):
    """
    A data model representing a collectible item in the abyss for ZZZ.

    Args:
        type (int): The type of the collectible item.
        cur_collect (int): The current amount of the collectible item.
        max_collect (int): The maximum amount of the collectible item.
    """

    type: int
    cur_collect: int
    max_collect: int


class ZZZAbyssNest(APIModel):
    """
    A data model representing an abyss nest for ZZZ.

    Args:
        is_nest (bool): A boolean indicating if it is an abyss nest.
    """

    is_nest: bool


class ZZZAbyssThrone(APIModel):
    """
    A data model representing an abyss throne for ZZZ.

    Args:
        is_throne (bool): A boolean indicating if it is an abyss throne.
        max_damage (str): The maximum damage associated with the throne.
    """

    is_throne: bool
    max_damage: str


class ZZZAbyssAbstract(APIModel):
    """
    A data model representing various aspects of the abyss for ZZZ.

    Args:
        abyss_level (ZZZAbyssLevel): A data model representing the abyss level.
        abyss_point (ZZZAbyssPoint): A data model representing the abyss point.
        abyss_duty (ZZZAbyssDuty): A data model representing the abyss duty.
        abyss_talent (ZZZAbyssTalent): A data model representing the abyss talent.
        refresh_time (datetime.timedelta): The time interval for refreshing the abyss.
        abyss_collect (List[ZZZAbyssCollectItem]): A list of collectible items in the abyss.
        abyss_nest (ZZZAbyssNest): A data model representing the abyss nest.
        abyss_throne (ZZZAbyssThrone): A data model representing the abyss throne.
        unlock (bool): A boolean indicating if the abyss is unlocked.
    """

    abyss_level: ZZZAbyssLevel
    abyss_point: ZZZAbyssPoint
    abyss_duty: ZZZAbyssDuty
    abyss_talent: ZZZAbyssTalent
    refresh_time: datetime.timedelta
    abyss_collect: List[ZZZAbyssCollectItem]
    abyss_nest: ZZZAbyssNest
    abyss_throne: ZZZAbyssThrone
    unlock: bool
