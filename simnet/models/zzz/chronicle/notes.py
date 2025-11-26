import datetime
import enum
from typing import Optional

from simnet.models.base import APIModel, TimeDeltaField


class ZZZNoteProgress(APIModel):
    """
    Represents the progress of the user.

    Attributes:
        max (int): The maximum progress of the user.
        current (int): The current progress of the user.
    """

    max: int
    current: int


class ZZZNoteEnergy(APIModel):
    """
    Represents the energy of the user.

    Attributes:
        progress (ZZZNoteProgress): The progress of the progress
        restore (int): The restore of the progress
        day_type (int): The day type of the progress
        hour (int): The hour of the progress
        minute (int): The minute of the progress
    """

    progress: ZZZNoteProgress
    restore: TimeDeltaField
    day_type: int
    hour: int
    minute: int


class ZZZNoteVitality(APIModel):
    """
    Represents the vitality of the user.

    Attributes:
        max (int): The maximum vitality of the user.
        current (int): The current vitality of the user.
    """

    max: int
    current: int


class ZZZNoteVhsSaleState(str, enum.Enum):
    """
    Represents the state of the vhs sale of the user.
    """

    FREE = "SaleStateNo"
    DOING = "SaleStateDoing"
    DONE = "SaleStateDone"


class ZZZNoteVhsSale(APIModel):
    """
    Represents the vhs sale of the user.

    Attributes:
        sale_state (ZZZNoteVhsSaleState): The state of the vhs sale of the user.
    """

    sale_state: ZZZNoteVhsSaleState


class ZZZNoteCardSignState(str, enum.Enum):
    """
    Represents the state of the card sign of the user.
    """

    FREE = "CardSignNo"
    DONE = "CardSignDone"


class ZZZNoteBountyCommission(APIModel):
    """
    A data model representing bounty commission for ZZZ notes.

    Args:
        num (int): The number of bounty commission.
        total (int): The total bounty commission.
        refresh_time (datetime.timedelta): The time until the bounty commission refreshes.
    """

    num: int
    total: int
    refresh_time: TimeDeltaField


class ZZZNoteSurveyPoints(APIModel):
    """
    A data model representing survey points for ZZZ notes.

    Args:
        num (int): The number of survey points.
        total (int): The total number of survey points.
        is_max_level (bool): A boolean indicating if the survey points are at the maximum level.
    """

    num: int
    total: int
    is_max_level: bool


class ZZZNoteWeeklyTask(APIModel):
    """
    Represents a weekly task in the ZZZ Note.

    Attributes:
        max_point (int): The maximum points for the weekly task.
        cur_point (int): The current points for the weekly task.
        refresh_time (datetime.timedelta): The time until the weekly task refreshes.
    """

    max_point: int
    cur_point: int
    refresh_time: TimeDeltaField


class ZZZNoteTempleRunningExpeditionState(str, enum.Enum):
    """
    Represents the state of the temple running expedition of the user.
    """

    Unknown = "ExpeditionStateUnknown"
    InProgress = "ExpeditionStateInProgress"
    InCanSend = "ExpeditionStateInCanSend"
    End = "ExpeditionStateEnd"


class ZZZNoteTempleRunningBenchState(str, enum.Enum):
    """
    Represents the state of the temple running bench of the user.
    """

    Unknown = "BenchStateUnknown"
    Producing = "BenchStateProducing"
    CanProduce = "BenchStateCanProduce"


class ZZZNoteTempleRunningShelveState(str, enum.Enum):
    """
    Represents the state of the temple running shelve of the user.
    """

    Unknown = "ShelveStateUnknown"
    Selling = "ShelveStateSelling"
    SoldOut = "ShelveStateSoldOut"
    CanSell = "ShelveStateCanSell"


class ZZZNoteTempleRunning(APIModel):
    """
    Represents the temple running state in the ZZZ Note.

    Attributes:
        expedition_state (ZZZNoteTempleRunningExpeditionState): The state of the temple running expedition.
        bench_state (ZZZNoteTempleRunningBenchState): The state of the temple running bench.
        shelve_state (ZZZNoteTempleRunningShelveState): The state of the temple running shelve.
        level (int): The level of the temple running.
        weekly_currency_max (int): The maximum weekly currency for the temple running.
        currency_next_refresh_ts (TimeDeltaField): The timestamp for the next currency refresh.
        current_currency (int): The current amount of currency in the temple running.
    """

    expedition_state: ZZZNoteTempleRunningExpeditionState
    bench_state: ZZZNoteTempleRunningBenchState
    shelve_state: ZZZNoteTempleRunningShelveState

    level: int
    weekly_currency_max: int
    currency_next_refresh_ts: TimeDeltaField
    current_currency: int


class ZZZNote(APIModel):
    """Represents a ZZZ Note.

    Attributes:
        energy (ZZZNoteEnergy): The energy of the user.
        vitality (ZZZNoteVitality): The vitality of the user.
        vhs_sale (ZZZNoteVhsSale): The vhs sale of the user.
        card_sign (ZZZNoteCardSignState): The card sign of the user.
        bounty_commission (ZZZNoteBountyCommission): The bounty commission of the user.
        survey_points (ZZZNoteSurveyPoints): The survey points of the user.
        weekly_task (ZZZNoteWeeklyTask): The weekly task of the user.
        temple_running (ZZZNoteTempleRunning): The temple running of the user.
        abyss_refresh (datetime.timedelta): The time until the abyss refreshes.
    """

    energy: ZZZNoteEnergy
    vitality: ZZZNoteVitality
    vhs_sale: ZZZNoteVhsSale
    card_sign: ZZZNoteCardSignState
    bounty_commission: Optional[ZZZNoteBountyCommission] = None
    survey_points: Optional[ZZZNoteSurveyPoints] = None
    weekly_task: Optional[ZZZNoteWeeklyTask] = None
    temple_running: Optional[ZZZNoteTempleRunning] = None
    abyss_refresh: TimeDeltaField

    @property
    def current_stamina(self) -> int:
        return self.energy.progress.current

    @property
    def max_stamina(self) -> int:
        return self.energy.progress.max

    @property
    def stamina_recover_time(self) -> datetime.datetime:
        """A property that returns the time when resin will be fully recovered."""
        return datetime.datetime.now().astimezone() + self.energy.restore

    @property
    def current_train_score(self) -> int:
        return self.vitality.current

    @property
    def max_train_score(self) -> int:
        return self.vitality.max
