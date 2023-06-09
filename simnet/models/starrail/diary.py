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
    """Diary category for rails_pass ."""

    id: str = Field(alias="action")
    name: str = Field(alias="action_name")
    amount: int = Field(alias="num")
    percentage: int = Field(alias="percent")


class MonthDiaryData(APIModel):
    """Diary data for a month."""

    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int
    hcoin_rate: int
    rails_rate: int
    categories: List[DiaryActionCategory] = Field(alias="group_by")


class DayDiaryData(APIModel):
    """Diary data for a day."""

    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int


class StarRailDiary(BaseDiary):
    """Traveler's diary."""

    data: MonthDiaryData = Field(alias="month_data")
    day_data: DayDiaryData

    @property
    def month_data(self) -> MonthDiaryData:
        return self.data
