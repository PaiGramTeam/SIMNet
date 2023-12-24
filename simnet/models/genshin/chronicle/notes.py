from datetime import timedelta, datetime
from enum import Enum
from typing import Union, Literal, Tuple, List, Optional, Dict, Any

from pydantic import Field, root_validator

from simnet.models.base import APIModel

__all__ = [
    "TaskRewardStatus",
    "TaskReward",
    "AttendanceRewardStatus",
    "AttendanceReward",
    "DailyTask",
    "Expedition",
    "Notes",
    "ExpeditionWidget",
    "NotesWidget",
    "NotesOverseaWidget",
    "NotesOverseaWidgetResin",
    "NotesOverseaWidgetRealm",
]


def _process_timedelta(time: Union[int, timedelta, datetime]) -> datetime:
    """A helper function that processes time inputs.

    Args:
        time (Union[int, timedelta, datetime]): The time input to process.

    Returns:
        datetime: The processed datetime.

    Raises:
        ValueError: If the input time is less than January 1, 2000.
    """
    if isinstance(time, int):
        time = datetime.fromtimestamp(time).astimezone()

    if isinstance(time, timedelta):
        time = datetime.now().astimezone() + time

    if time < datetime(2000, 1, 1).astimezone():
        delta = timedelta(seconds=int(time.timestamp()))
        time = datetime.now().astimezone() + delta

    time = time.replace(second=0, microsecond=0)

    return time


class Expedition(APIModel):
    """The model for a real-time expedition.

    Attributes:
        character (str): The expedition character icon url.
        status (Literal["Ongoing", "Finished"]): The status of the expedition.
        remaining_time (timedelta): The remaining time of the expedition.
    """

    character: str = Field(alias="avatar_side_icon")
    status: Literal["Ongoing", "Finished"]
    remaining_time: timedelta = Field(alias="remained_time")

    @property
    def finished(self) -> bool:
        """A property that returns whether the expedition has finished."""
        return self.remaining_time <= timedelta(0)

    @property
    def completion_time(self) -> datetime:
        """A property that returns the completion time of the expedition."""
        return datetime.now().astimezone() + self.remaining_time


class TransformerTimedelta(timedelta):
    """The model for a transformer recovery time."""

    @property
    def timedata(self) -> Tuple[int, int, int, int]:
        """A property that returns the transformer recovery time in days, hours, minutes, and seconds."""
        seconds: int = super().seconds
        days: int = super().days
        hour, second = divmod(seconds, 3600)
        minute, second = divmod(second, 60)

        return days, hour, minute, second

    @property
    def hours(self) -> int:
        """A property that returns the transformer recovery time in hours."""
        return self.timedata[1]

    @property
    def minutes(self) -> int:
        """A property that returns the transformer recovery time in minutes."""
        return self.timedata[2]

    @property
    def seconds(self) -> int:
        """A property that returns the transformer recovery time in seconds."""
        return self.timedata[3]


class TaskRewardStatus(str, Enum):
    """The enum for task reward statuses."""

    Invalid = "TaskRewardStatusInvalid"
    TakenAward = "TaskRewardStatusTakenAward"
    Finished = "TaskRewardStatusFinished"
    Unfinished = "TaskRewardStatusUnfinished"


class TaskReward(APIModel):
    """The model for a task reward.

    Attributes:
        status (TaskRewardStatus): The status of the task reward.
    """

    status: TaskRewardStatus


class AttendanceRewardStatus(str, Enum):
    """The enum for attendance reward statuses."""

    Invalid = "AttendanceRewardStatusInvalid"
    TakenAward = "AttendanceRewardStatusTakenAward"
    WaitTaken = "AttendanceRewardStatusWaitTaken"
    Unfinished = "AttendanceRewardStatusUnfinished"
    FinishedNonReward = "AttendanceRewardStatusFinishedNonReward"
    Forbid = "AttendanceRewardStatusForbid"


class AttendanceReward(APIModel):
    """The model for an attendance reward.

    Attributes:
        status (AttendanceRewardStatus): The status of the attendance reward.
        progress (int): The progress of the attendance reward.
    """

    status: AttendanceRewardStatus
    progress: int


class DailyTask(APIModel):
    """The model for a daily task.

    Attributes:
        total_num (int): The total number of daily tasks.
        finished_num (int): The number of finished daily tasks.
        is_extra_task_reward_received (bool): Whether the extra task reward has been received.
        task_rewards (List[TaskReward]): The list of task rewards.
        attendance_rewards (List[AttendanceReward]): The list of attendance rewards.
        attendance_visible (bool): Whether the attendance rewards are visible.
    """

    total_num: int
    finished_num: int
    is_extra_task_reward_received: bool
    task_rewards: List[TaskReward]
    attendance_rewards: List[AttendanceReward]
    attendance_visible: bool


class ArchonStatusEnum(str, Enum):
    """The enum for archon statuses."""

    StatusFinished = "StatusFinished"
    StatusOngoing = "StatusOngoing"
    StatusNotOpen = "StatusNotOpen"


class ArchonStatus(APIModel):
    """The model for archon status.

    Attributes:
        status (ArchonStatusEnum): The status of the archon.
        chapter_num (str): The chapter number.
        chapter_title (str): The chapter title.
        id (int): The archon id.
    """

    status: ArchonStatusEnum
    chapter_num: str
    chapter_title: str
    id: int


class ArchonQuestProgress(APIModel):
    """The model for archon quest progress.

    Attributes:
        list (List[ArchonStatus]): The list of archon status.
        is_open_archon_quest (bool): Whether the archon quest is open. (魔神任务)
        is_finish_all_mainline (bool): Whether all mainline quests are finished. (主线)
        is_finish_all_interchapter (bool): Whether all interchapter quests are finished. (间章)
        wiki_url (str): The wiki url.
    """

    list: List[ArchonStatus]
    is_open_archon_quest: bool
    is_finish_all_mainline: bool
    is_finish_all_interchapter: bool
    wiki_url: str

    @property
    def all_completed(self) -> bool:
        return self.is_finish_all_mainline and self.is_finish_all_interchapter


class Notes(APIModel):
    """The model for real-time notes.

    Attributes:
        current_resin (int): The current amount of resin.
        max_resin (int): The maximum amount of resin.
        remaining_resin_recovery_time (timedelta): The remaining time until resin recovery.
        current_realm_currency (int): The current amount of realm currency.
        max_realm_currency (int): The maximum amount of realm currency.
        remaining_realm_currency_recovery_time (timedelta): The remaining time until realm currency recovery.
        completed_commissions (int): The number of completed commissions.
        max_commissions (int): The maximum number of commissions.
        claimed_commission_reward (bool): Whether the commission reward has been claimed.
        remaining_resin_discounts (int): The number of remaining resin discounts.
        max_resin_discounts (int): The maximum number of resin discounts.
        remaining_transformer_recovery_time (Optional[TransformerTimedelta]): The remaining time until
            transformer recovery.
        expeditions (List[Expedition]): The list of expeditions.
        max_expeditions (int): The maximum number of expeditions.

    Raises:
        ValueError: If the remaining resin recovery time is less than 0 or greater than 8 hours,
            or if the remaining realm currency recovery time is less than 0 or greater than 24 hours.
    """

    current_resin: int
    max_resin: int
    remaining_resin_recovery_time: timedelta = Field(alias="resin_recovery_time")

    current_realm_currency: int = Field(alias="current_home_coin")
    max_realm_currency: int = Field(alias="max_home_coin")
    remaining_realm_currency_recovery_time: timedelta = Field(alias="home_coin_recovery_time")

    completed_commissions: int = Field(alias="finished_task_num")
    max_commissions: int = Field(alias="total_task_num")
    claimed_commission_reward: bool = Field(alias="is_extra_task_reward_received")

    remaining_resin_discounts: int = Field(alias="remain_resin_discount_num")
    max_resin_discounts: int = Field(alias="resin_discount_num_limit")

    remaining_transformer_recovery_time: Optional[TransformerTimedelta]

    expeditions: List[Expedition]
    max_expeditions: int = Field(alias="max_expedition_num")

    daily_task: DailyTask
    archon_quest_progress: ArchonQuestProgress

    @property
    def resin_recovery_time(self) -> datetime:
        """A property that returns the time when resin will be fully recovered."""
        return datetime.now().astimezone() + self.remaining_resin_recovery_time

    @property
    def realm_currency_recovery_time(self) -> datetime:
        """A property that returns the time when realm currency will be fully recovered."""
        return datetime.now().astimezone() + self.remaining_realm_currency_recovery_time

    @property
    def transformer_recovery_time(self) -> Optional[datetime]:
        """A property that returns the time when the transformer will be fully recovered."""
        if self.remaining_transformer_recovery_time is None:
            return None

        remaining = datetime.now().astimezone() + self.remaining_transformer_recovery_time
        return remaining

    @root_validator(pre=True)
    def flatten_transformer(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """A validator that flattens the transformer recovery time.

        This method flattens the transformer recovery time from a dictionary format to a TransformerTimedelta format.

        Args:
            values (Dict[str, Any]): The input values.

        Returns:
            Dict[str, Any]: The values with the transformer recovery time flattened.

        Raises:
            ValueError: If the transformer recovery time is less than 0 or greater than 7 days.
        """
        if "transformer_recovery_time" in values:
            return values

        if values.get("transformer") and values["transformer"]["obtained"]:
            t = values["transformer"]["recovery_time"]
            delta = TransformerTimedelta(days=t["Day"], hours=t["Hour"], minutes=t["Minute"], seconds=t["Second"])
            values["remaining_transformer_recovery_time"] = delta
        else:
            values["remaining_transformer_recovery_time"] = None

        if (
            values["remaining_transformer_recovery_time"] is not None
            and values["remaining_transformer_recovery_time"].days > 7
        ):
            raise ValueError("Transformer recovery time cannot exceed 7 days.")

        return values


class ExpeditionWidget(APIModel):
    """The model for a real-time expedition.

    Attributes:
        character (str): The expedition character icon url.
        status (Literal["Ongoing", "Finished"]): The status of the expedition.
    """

    character: str = Field(alias="avatar_side_icon")
    status: Literal["Ongoing", "Finished"]


class NotesWidget(APIModel):
    """The model for real-time notes.

    Attributes:
        current_resin (int): The current amount of resin.
        max_resin (int): The maximum amount of resin.
        remaining_resin_recovery_time (timedelta): The remaining time until resin recovery.
        current_realm_currency (int): The current amount of realm currency.
        max_realm_currency (int): The maximum amount of realm currency.
        completed_commissions (int): The number of completed commissions.
        max_commissions (int): The maximum number of commissions.
        claimed_commission_reward (bool): Whether the commission reward has been claimed.
        expeditions (List[Expedition]): The list of expeditions.
        max_expeditions (int): The maximum number of expeditions.

    Raises:
        ValueError: If the remaining resin recovery time is less than 0 or greater than 8 hours,
            or if the remaining realm currency recovery time is less than 0 or greater than 24 hours.
    """

    current_resin: int
    max_resin: int
    remaining_resin_recovery_time: timedelta = Field(alias="resin_recovery_time")

    current_realm_currency: int = Field(alias="current_home_coin")
    max_realm_currency: int = Field(alias="max_home_coin")

    completed_commissions: int = Field(alias="finished_task_num")
    max_commissions: int = Field(alias="total_task_num")
    claimed_commission_reward: bool = Field(alias="is_extra_task_reward_received")

    expeditions: List[ExpeditionWidget]
    max_expeditions: int = Field(alias="max_expedition_num")

    @property
    def resin_recovery_time(self) -> datetime:
        """A property that returns the time when resin will be fully recovered."""
        return datetime.now().astimezone() + self.remaining_resin_recovery_time


class NotesOverseaWidgetResin(APIModel):
    """The model for real-time notes resin.

    Attributes:
        current_val (int): The current amount of resin.
        max_val (int): The maximum amount of resin.
        remaining_resin_recovery_time (timedelta): The remaining time until resin recovery.
    """

    current_val: int
    max_val: int
    remaining_resin_recovery_time: timedelta = Field(alias="recovery_time")

    @property
    def resin_recovery_time(self) -> datetime:
        """A property that returns the time when resin will be fully recovered."""
        return datetime.now().astimezone() + self.remaining_resin_recovery_time


class NotesOverseaWidgetRealm(APIModel):
    """The model for real-time notes realm currency.

    Attributes:
        current_val (int): The current amount of realm currency.
        max_val (int): The maximum amount of realm currency.
        remaining_realm_currency_recovery_time (timedelta): The remaining time until realm currency recovery.
    """

    current_val: int
    max_val: int
    remaining_realm_currency_recovery_time: timedelta = Field(alias="recovery_time")

    @property
    def realm_currency_recovery_time(self) -> datetime:
        """A property that returns the time when realm currency will be fully recovered."""
        return datetime.now().astimezone() + self.remaining_realm_currency_recovery_time


class NotesOverseaWidget(APIModel):
    """The model for real-time notes.

    Attributes:
        resin (NotesOverseaWidgetResin): The resin information.
        home_coin (NotesOverseaWidgetRealm): The realm currency information.

    Raises:
        ValueError: If the remaining resin recovery time is less than 0 or greater than 8 hours,
            or if the remaining realm currency recovery time is less than 0 or greater than 24 hours.
    """

    resin: NotesOverseaWidgetResin
    home_coin: NotesOverseaWidgetRealm
