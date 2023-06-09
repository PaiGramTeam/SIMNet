from typing import List

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.diary import BaseDiary

__all__ = (
    "DiaryActionCategory",
    "MonthDiaryData",
    "DayDiaryData",
    "StarRailDiary",
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


class MonthDiaryData(APIModel):
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

    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int
    hcoin_rate: int
    rails_rate: int
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

    @property
    def month_data(self) -> MonthDiaryData:
        """Diary data for a month."""
        return self.data
