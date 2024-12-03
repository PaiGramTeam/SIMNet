from simnet.models.base import APIModel, Field
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
        action: Category name.
        amount: Amount of rails_pass.
        percentage: Percentage of rails_pass.
    """

    action: str
    amount: int = Field(alias="num")
    percentage: int = Field(alias="percent")

    @property
    def name(self) -> str:
        return {
            "growth_rewards": "成长奖励",
            "daily_activity_rewards": "日常活跃奖励",
            "mail_rewards": "邮件奖励",
            "event_rewards": "活动奖励",
            "hollow_rewards": "零号空洞奖励",
            "shiyu_rewards": "式舆防卫战奖励",
            "other_rewards": "其他奖励",
        }.get(self.action, "其他奖励")


class ZZZMonthDiaryData(APIModel):
    """Diary data for a month.

    Attributes:
        categories: List of diary categories.
    """

    list: list[ZZZDiaryDataList]
    categories: list[ZZZDiaryActionCategory] = Field(alias="income_components")


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
    optional_month: list[str]
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
