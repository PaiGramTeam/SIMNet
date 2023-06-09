from datetime import timedelta, datetime
from typing import List, Literal, Sequence

from simnet.models.base import APIModel


class StarRailExpedition(APIModel):
    """Represents a StarRail Expedition.

    Attributes:
        avatars (List[str]): A list of avatar names participating in the expedition.
        status (Literal["Ongoing", "Finished"]): The status of the expedition.
        remaining_time (timedelta): The time remaining for the expedition to finish.
        name (str): The name of the expedition.

    """

    avatars: List[str]
    status: Literal["Ongoing", "Finished"]
    remaining_time: timedelta
    name: str

    @property
    def finished(self) -> bool:
        """Returns whether the expedition has finished."""
        return self.remaining_time <= timedelta(0)

    @property
    def completion_time(self) -> datetime:
        """Returns the time at which the expedition will be completed."""
        return datetime.now().astimezone() + self.remaining_time


class StarRailNote(APIModel):
    """Represents a StarRail Note.

    Attributes:
        current_stamina (int): The current stamina of the user.
        max_stamina (int): The maximum stamina of the user.
        stamina_recover_time (timedelta): The time it takes for one stamina to recover.
        accepted_epedition_num (int): The number of expeditions the user has accepted.
        total_expedition_num (int): The total number of expeditions the user has participated in.
        expeditions (Sequence[StarRailExpedition]): A list of expeditions the user has participated in.

    """

    current_stamina: int
    max_stamina: int
    stamina_recover_time: timedelta
    accepted_epedition_num: int
    total_expedition_num: int
    expeditions: Sequence[StarRailExpedition]
