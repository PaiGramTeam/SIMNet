import datetime
import enum

from simnet.models.base import APIModel


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
    """

    progress: ZZZNoteProgress
    restore: datetime.timedelta


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


class ZZZNote(APIModel):
    """Represents a ZZZ Note.

    Attributes:
        energy (ZZZNoteEnergy): The energy of the user.
        vitality (ZZZNoteVitality): The vitality of the user.
        vhs_sale (ZZZNoteVhsSale): The vhs sale of the user.
    """

    energy: ZZZNoteEnergy
    vitality: ZZZNoteVitality
    vhs_sale: ZZZNoteVhsSale

    @property
    def current_stamina(self) -> int:
        return self.energy.progress.current

    @property
    def max_stamina(self) -> int:
        return self.energy.progress.max

    @property
    def stamina_recover_time(self) -> datetime:
        """A property that returns the time when resin will be fully recovered."""
        return datetime.datetime.now().astimezone() + self.energy.restore

    @property
    def current_train_score(self) -> int:
        return self.vitality.current

    @property
    def max_train_score(self) -> int:
        return self.vitality.max
