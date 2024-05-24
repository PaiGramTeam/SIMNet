from typing import List

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.diary import BaseDiary
from simnet.models.starrail.chronicle.base import PartialTime

__all__ = (
    "DiaryActionCategory",
    "StarRailMonthDiaryDataBase",
    "MonthDiaryData",
    "DayDiaryData",
    "StarRailDiary",
    "StarRailLedgerMonthInfo",
)


class DiaryActionCategory(APIModel):
    """Diary category for rails_pass .

    Attributes:
        id: Category ID.
        name: Category name.
        amount: Amount of rails_pass.
        percentage: Percentage of rails_pass.
    """

    id: str = Field(alias="action")
    name: str = Field(alias="action_name")
    amount: int = Field(alias="num")
    percentage: int = Field(alias="percent")


class StarRailMonthDiaryDataBase(APIModel):
    """Diary base data for a month.

    Attributes:
        current_hcoin: Current amount of hcoin.
        current_rails_pass: Current amount of rails_pass.
        last_hcoin: Last amount of hcoin.
        last_rails_pass: Last amount of rails_pass.
        hcoin_rate: hcoin rate.
        rails_rate: rails_pass rate.
    """

    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int
    hcoin_rate: int
    rails_rate: int


class MonthDiaryData(StarRailMonthDiaryDataBase):
    """Diary data for a month.

    Attributes:
        current_hcoin: Current amount of hcoin.
        current_rails_pass: Current amount of rails_pass.
        last_hcoin: Last amount of hcoin.
        last_rails_pass: Last amount of rails_pass.
        hcoin_rate: hcoin rate.
        rails_rate: rails_pass rate.
        categories: List of diary categories.
    """

    categories: List[DiaryActionCategory] = Field(alias="group_by")


class DayDiaryData(APIModel):
    """Diary data for a day.

    Attributes:
        current_hcoin: Current amount of hcoin.
        current_rails_pass: Current amount of rails_pass.
        last_hcoin: Last amount of hcoin.
        last_rails_pass: Last amount of rails_pass.
    """

    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int


class StarRailDiary(BaseDiary):
    """Traveler's diary.

    Attributes:
        data: Diary data for a month.
        day_data: Diary data for a day.
    """

    data: MonthDiaryData = Field(alias="month_data")
    day_data: DayDiaryData
    version: str
    optional_month: List[str]
    current_month: str = Field(alias="month")
    start_month: str

    @property
    def data_id(self) -> int:
        """Get the data ID."""
        return self.month

    @property
    def month_data(self) -> MonthDiaryData:
        """Diary data for a month."""
        return self.data


class StarRailLedgerMonthInfo(StarRailMonthDiaryDataBase):
    """Ledger month info.

    Attributes:
        current_hcoin: Current amount of hcoin.
        current_rails_pass: Current amount of rails_pass.
        last_hcoin: Last amount of hcoin.
        last_rails_pass: Last amount of rails_pass.
        hcoin_rate: hcoin rate.
        rails_rate: rails_pass rate.
        time: PartialTime
    """

    time: PartialTime
