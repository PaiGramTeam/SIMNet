from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Literal, Optional

from simnet.models.base import APIModel, DateTimeField, Field, TimeDeltaField


class StarRailExpedition(APIModel):
    """Represents a StarRail Expedition.

    Attributes:
        avatars (List[str]): A list of avatar names participating in the expedition.
        status (Literal["Ongoing", "Finished"]): The status of the expedition.
        remaining_time (timedelta): The time remaining for the expedition to finish.
        finish_ts (datetime): The timestamp when the expedition will finish.
        name (str): The name of the expedition.
        item_url (Optional[str]): The URL of the expedition item, if available.
    """

    avatars: list[str]
    status: Literal["Ongoing", "Finished"]
    remaining_time: TimeDeltaField
    finish_ts: Optional[DateTimeField] = None
    name: str
    item_url: Optional[str] = None

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
        current_ts (datetime): The current timestamp.

        current_stamina (int): The current stamina of the user.
        max_stamina (int): The maximum stamina of the user.
        stamina_recover_time (timedelta): The time it takes for one stamina to recover.
        stamina_full_ts (datetime): The timestamp when the stamina will be full.

        accepted_epedition_num (int): The number of expeditions the user has accepted.
        total_expedition_num (int): The total number of expeditions the user has participated in.
        expeditions (Sequence[StarRailExpedition]): A list of expeditions the user has participated in.

        current_train_score (int): The current daily training activity.
        max_train_score (int): The max daily training activity.

        current_rogue_score (int): The current simulated universe weekly points.
        max_rogue_score (int): The max simulated universe weekly points.

        remaining_weekly_discounts (int): The remaining echo of war rewards.
        max_weekly_discounts (int): The echo of war attempt limit.

        current_reserve_stamina (int): The current reserve stamina.
        is_reserve_stamina_full (bool): Whether the reserve stamina is full.
    """

    current_ts: DateTimeField

    current_stamina: int
    max_stamina: int
    stamina_recover_time: TimeDeltaField
    stamina_full_ts: DateTimeField

    accepted_epedition_num: int
    total_expedition_num: int
    expeditions: Sequence[StarRailExpedition]

    current_train_score: int
    """Current daily training activity"""
    max_train_score: int
    """Max daily training activity"""

    current_rogue_score: int
    """Current simulated universe weekly points"""
    max_rogue_score: int
    """Max simulated universe weekly points"""

    remaining_weekly_discounts: int = Field(alias="weekly_cocoon_cnt")
    """Remaining echo of war rewards"""
    max_weekly_discounts: int = Field(alias="weekly_cocoon_limit")
    """Echo of war attempt limit"""

    current_reserve_stamina: int
    """Current reserve stamina"""
    is_reserve_stamina_full: bool
    """Whether the reserve stamina is full"""

    rogue_tourn_weekly_unlocked: bool
    """Whether the rogue tournament is unlocked"""
    rogue_tourn_weekly_max: int
    """The max number of rogue tournament attempts"""
    rogue_tourn_weekly_cur: int
    """The current number of rogue tournament attempts"""
    rogue_tourn_exp_is_full: bool
    """Whether the rogue tournament expedition is full"""

    grid_fight_weekly_cur: int
    """The current number of grid fight attempts"""
    grid_fight_weekly_max: int
    """The max number of grid fight attempts"""


class StarRailNoteWidget(APIModel):
    """Represents a StarRail Note.

    Attributes:
        current_stamina (int): The current stamina of the user.
        max_stamina (int): The maximum stamina of the user.
        stamina_recover_time (timedelta): The time it takes for one stamina to recover.
        current_reserve_stamina (int): The current reserve stamina.
        is_reserve_stamina_full (bool): Whether the reserve stamina is full.
        accepted_expedition_num (int): The number of expeditions the user has accepted.
        total_expedition_num (int): The total number of expeditions the user has participated in.
        expeditions (Sequence[StarRailExpedition]): A list of expeditions the user has participated in.
        current_train_score (int): The current daily training activity.
        max_train_score (int): The max daily training activity.
        current_rogue_score (int): The current simulated universe weekly points.
        max_rogue_score (int): The max simulated universe weekly points.
        has_signed (bool): Whether the user has signed in today.
    """

    current_stamina: int
    max_stamina: int
    stamina_recover_time: TimeDeltaField
    current_reserve_stamina: int
    is_reserve_stamina_full: bool
    accepted_expedition_num: int
    total_expedition_num: int
    expeditions: Sequence[StarRailExpedition]

    current_train_score: int
    """Current daily training activity"""
    max_train_score: int
    """Max daily training activity"""

    current_rogue_score: int
    """Current simulated universe weekly points"""
    max_rogue_score: int
    """Max simulated universe weekly points"""

    has_signed: bool
    """Whether the user has signed in today"""

    rogue_tourn_weekly_unlocked: bool
    """Whether the rogue tournament is unlocked"""
    rogue_tourn_weekly_max: int
    """The max number of rogue tournament attempts"""
    rogue_tourn_weekly_cur: int
    """The current number of rogue tournament attempts"""


class StarRailNoteOverseaWidgetChallenge(APIModel):
    """Represents a StarRail Note.

    Attributes:
        begin_time (datetime): The time at which the challenge begins.
        current_floor (int): The current floor of the challenge.
        end_time (datetime): The time at which the challenge ends.
        max_floor (int): The max floor of the challenge.
        schedule_id (int): The ID of the challenge.
    """

    begin_time: datetime
    """The time at which the challenge begins."""
    current_floor: int
    """The current floor of the challenge."""
    end_time: datetime
    """The time at which the challenge ends."""
    max_floor: int
    """The max floor of the challenge."""
    schedule_id: int
    """The ID of the challenge."""


class StarRailNoteOverseaWidgetRogue(APIModel):
    """Represents a StarRail Note.

    Attributes:
        current_rogue_score (int): The current simulated universe weekly points.
        max_rogue_score (int): The max simulated universe weekly points.
        schedule_end (datetime): The time at which the challenge ends.
        schedule_start (datetime): The time at which the challenge begins.
    """

    current_rogue_score: int
    """Current simulated universe weekly points"""
    max_rogue_score: int
    """Max simulated universe weekly points"""
    schedule_end: datetime
    """The time at which the challenge ends."""
    schedule_start: datetime
    """The time at which the challenge begins."""


class StarRailNoteOverseaWidget(APIModel):
    """Represents a StarRail Note.

    Attributes:
        current_stamina (int): The current stamina of the user.
        max_stamina (int): The maximum stamina of the user.
        stamina_recover_time (timedelta): The time it takes for one stamina to recover.
        accepted_expedition_num (int): The number of expeditions the user has accepted.
        total_expedition_num (int): The total number of expeditions the user has participated in.
        expeditions (Sequence[StarRailExpedition]): A list of expeditions the user has participated in.
        current_train_score (int): The current daily training activity.
        max_train_score (int): The max daily training activity.
        challenge (StarRailNoteOverseaWidgetChallenge): The challenge widget.
        rogue (StarRailNoteOverseaWidgetRogue): The rogue widget.
    """

    current_stamina: int
    max_stamina: int
    stamina_recover_time: TimeDeltaField
    accepted_expedition_num: int
    total_expedition_num: int
    expeditions: Sequence[StarRailExpedition]

    current_train_score: int
    """Current daily training activity"""
    max_train_score: int
    """Max daily training activity"""

    challenge: StarRailNoteOverseaWidgetChallenge
    """The challenge widget."""
    rogue: StarRailNoteOverseaWidgetRogue
    """The rogue widget."""
