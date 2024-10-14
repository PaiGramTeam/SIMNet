from typing import List

from simnet.models.base import APIModel


class StarRailAchievementInfoList(APIModel):
    """
    Represents a list of achievement information for Star Rail.

    Attributes:
        series_id (int): The ID of the achievement series.
        name (str): The name of the achievement.
        icon (str): The icon representing the achievement.
        cur (int): The current progress of the achievement.
        max (int): The maximum progress required for the achievement.
    """

    series_id: int
    name: str
    icon: str
    cur: int
    max: int

    @property
    def percentage(self) -> float:
        """
        Calculates the completion percentage of the achievement.

        Returns:
            float: The completion percentage of the achievement.
        """
        return round(self.cur * 1.00 / self.max * 100, 2)


class StarRailAchievementInfo(APIModel):
    """
    Represents the achievement information for Star Rail.

    Attributes:
        gold_num (int): The number of gold achievements.
        silver_num (int): The number of silver achievements.
        copper_num (int): The number of copper achievements.
        list (List[StarRailAchievementInfoList]): A list of achievement info objects.
        strategy_url (str): The URL for the achievement strategy.
    """

    gold_num: int
    silver_num: int
    copper_num: int
    list: List[StarRailAchievementInfoList]
    strategy_url: str
