import datetime
from typing import NamedTuple

from simnet.models.base import APIModel, Field, DateTimeField, CN_TIMEZONE

__all__ = ("ClaimedDailyReward", "DailyReward", "DailyRewardInfo")


class DailyRewardInfo(NamedTuple):
    """Information about the current daily reward status.

    Attributes:
        signed_in (bool): Whether the user has signed in today.
        claimed_rewards (int): The number of rewards claimed today.
    """

    signed_in: bool
    claimed_rewards: int

    @property
    def missed_rewards(self) -> int:
        """The number of rewards that the user has missed since the start of the month."""
        now = datetime.datetime.now(CN_TIMEZONE)
        return now.day - self.claimed_rewards


class DailyReward(APIModel):
    """Claimable daily reward.

    Attributes:
        name (str): The name of the reward.
        amount (int): The amount of the reward.
        icon (str): The URL of the icon for the reward.
    """

    name: str
    amount: int = Field(alias="cnt")
    icon: str


class ClaimedDailyReward(APIModel):
    """Claimed daily reward.

    Attributes:
        id (int): The ID of the claimed reward.
        name (str): The name of the reward.
        amount (int): The amount of the reward.
        icon (str): The URL of the icon for the reward.
        time (datetime): The time at which the reward was claimed.
    """

    id: int
    name: str
    amount: int = Field(alias="cnt")
    icon: str = Field(alias="img")
    time: DateTimeField = Field(alias="created_at")
