from datetime import datetime
from typing import List

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.diary import BaseDiary

__all__ = (
    "DayDiaryData",
    "Diary",
    "DiaryAction",
    "DiaryActionCategory",
    "DiaryPage",
    "MonthDiaryData",
)


class DiaryActionCategory(APIModel):
    """Diary category for primogems."""

    id: int = Field(alias="action_id")
    name: str = Field(alias="action")
    amount: int = Field(alias="num")
    percentage: int = Field(alias="percent")


class MonthDiaryData(APIModel):
    """Diary data for a month."""

    current_primogems: int
    current_mora: int
    last_primogems: int
    last_mora: int
    primogems_rate: int = Field(alias="primogem_rate")
    mora_rate: int
    categories: List[DiaryActionCategory] = Field(alias="group_by")


class DayDiaryData(APIModel):
    """Diary data for a day."""

    current_primogems: int
    current_mora: int


class Diary(BaseDiary):
    """Traveler's diary."""

    data: MonthDiaryData = Field(alias="month_data")
    day_data: DayDiaryData

    @property
    def month_data(self) -> MonthDiaryData:
        return self.data


class DiaryAction(APIModel):
    """Action which earned currency."""

    action_id: int
    action: str
    time: datetime = Field(timezone=8)
    amount: int = Field(alias="num")


class DiaryPage(BaseDiary):
    """Page of a diary."""

    actions: List[DiaryAction] = Field(alias="list")
