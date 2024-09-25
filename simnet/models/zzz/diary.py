from typing import List

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.diary import BaseDiary

__all__ = (
    "ZZZDiaryDataList",
    "ZZZDiaryActionCategory",
    "ZZZMonthDiaryData",
    "ZZZDiary",
)


class ZZZDiaryDataList(APIModel):
    """List of diary data.

    Attributes:
        id: Data ID.
        name: Data name.
        amount: Amount of data.
    """

    id: str = Field(alias="data_type")
    name: str = Field(alias="data_name")
    amount: int = Field(alias="count")


class ZZZDiaryActionCategory(APIModel):
    """Diary category for PolychromesData .

    Attributes:
        name: Category name.
        amount: Amount of rails_pass.
        percentage: Percentage of rails_pass.
    """

    name: str = Field(alias="action")
    amount: int = Field(alias="num")
    percentage: int = Field(alias="percent")


class ZZZMonthDiaryData(APIModel):
    """Diary data for a month.

    Attributes:
        categories: List of diary categories.
    """

    list: List[ZZZDiaryDataList]
    categories: List[ZZZDiaryActionCategory] = Field(alias="income_components")


class ZZZDiaryRoleInfo(APIModel):
    """Role info for a diary."""

    nickname: str
    avatar: str


class ZZZDiary(BaseDiary):
    """Traveler's diary.

    Attributes:
        data: Diary data for a month.
        optional_month: Optional month.
        current_month: Current month.
        data_month: Data month.
    """

    data: ZZZMonthDiaryData = Field(alias="month_data")
    optional_month: List[str]
    current_month: str
    data_month: str
    role_info: ZZZDiaryRoleInfo

    @property
    def data_id(self) -> int:
        """Get the data ID."""
        return self.month

    @property
    def month_data(self) -> ZZZMonthDiaryData:
        """Diary data for a month."""
        return self.data
