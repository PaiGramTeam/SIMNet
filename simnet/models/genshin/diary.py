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
    """Diary category for primogems.

    Attributes:
        id: Category ID.
        name: Category name.
        amount: Amount of primogems.
        percentage: Percentage of primogems.
    """

    id: int = Field(alias="action_id")
    name: str = Field(alias="action")
    amount: int = Field(alias="num")
    percentage: int = Field(alias="percent")


class MonthDiaryData(APIModel):
    """Diary data for a month.

    Attributes:
        current_primogems: Current amount of primogems.
        current_mora: Current amount of mora.
        last_primogems: Last amount of primogems.
        last_mora: Last amount of mora.
        primogems_rate: Primogems rate.
        mora_rate: Mora rate.
        categories: List of diary categories.
    """

    current_primogems: int
    current_mora: int
    last_primogems: int
    last_mora: int
    primogems_rate: int = Field(aliases="primogem_rate")
    mora_rate: int
    categories: List[DiaryActionCategory] = Field(alias="group_by")


class DayDiaryData(APIModel):
    """Diary data for a day.

    Attributes:
        current_primogems: Current amount of primogems.
        current_mora: Current amount of mora.
    """

    current_primogems: int
    current_mora: int


class Diary(BaseDiary):
    """Traveler's diary.

    Attributes:
        data: Diary data for a month.
        day_data: Diary data for a day.
    """

    data: MonthDiaryData = Field(alias="month_data")
    day_data: DayDiaryData

    @property
    def month_data(self) -> MonthDiaryData:
        return self.data


class DiaryAction(APIModel):
    """Action which earned currency.

    Attributes:
        action_id: Action ID.
        action: Action name.
        time: Time of the action.
        amount: Amount of the action.
    """

    action_id: int
    action: str
    time: datetime = Field(timezone=8)
    amount: int = Field(alias="num")


class DiaryPage(BaseDiary):
    """Page of a diary.

    Attributes:
        actions: List of diary actions.
    """

    actions: List[DiaryAction] = Field(alias="list")
