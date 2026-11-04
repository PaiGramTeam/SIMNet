from simnet.models.base import APIModel, TimeDeltaField
from simnet.models.zzz.chronicle.abyss_abstract import ZZZAbyssCollectItem, ZZZAbyssDuty, ZZZAbyssLevel


class ZZZAbyssTask(APIModel):
    """
    Represents a task in the ZZZAbyss.

    Attributes:
        cur_task (int): The current task number.
        max_task (int): The maximum task number.
    """

    cur_task: int
    max_task: int


class ZZZAbyssMax(APIModel):
    """
    Represents the maximum attributes in the ZZZAbyss.

    Attributes:
        max_name (str): The name of the maximum attribute.
        heat_count (int): The count of heat.
        max_count (int): The maximum count.
        best_time (int): The best time recorded.
        has_data (bool): Indicates if data is available.
    """

    max_name: str
    heat_count: int
    max_count: int
    best_time: int
    has_data: bool


class ZZZAbysss2Abstract(APIModel):
    """
    Represents the abstract attributes of the ZZZAbyss.

    Attributes:
        abyss_level (Optional[ZZZAbyssLevel]): The level of the abyss.
        abyss_task (Optional[ZZZAbyssTask]): The task in the abyss.
        abyss_duty (Optional[ZZZAbyssDuty]): The duty in the abyss.
        refresh_time (TimeDeltaField): The refresh time of the abyss.
        abyss_max (Optional[ZZZAbyssMax]): The maximum attributes in the abyss.
        abyss_collect (list[ZZZAbyssCollectItem]): The collection of items in the abyss.
        unlock (bool): Indicates if the abyss is unlocked.
    """

    abyss_level: ZZZAbyssLevel | None = None
    abyss_task: ZZZAbyssTask | None = None
    abyss_duty: ZZZAbyssDuty | None = None
    refresh_time: TimeDeltaField
    abyss_max: ZZZAbyssMax | None = None
    abyss_collect: list[ZZZAbyssCollectItem]
    unlock: bool
