from simnet.models.base import APIModel


class GenshinAchievementInfoList(APIModel):
    """
    Represents a list of achievement information for Genshin.

    Attributes:
        id (int): The unique identifier of the achievement.
        name (str): The name of the achievement.
        icon (str): The URL or path to the icon representing the achievement.
        finish_num (int): The number of times the achievement has been completed.
        percentage (int): The completion percentage of the achievement.
        show_percent (bool): Indicates whether the percentage should be displayed.
    """

    id: int
    name: str
    icon: str
    finish_num: int
    percentage: int
    show_percent: bool

    @property
    def max(self) -> int:
        """
        Calculates the maximum number of times the achievement can be completed.

        Returns:
            int: The maximum completion value if `show_percent` is True, otherwise 0.
        """
        return round(self.finish_num / (self.percentage / 100.0)) if self.percentage else 0


class GenshinAchievementInfo(APIModel):
    """
    Represents the achievement information for Genshin.

    Attributes:
        achievement_num (int): The number of owned achievements.
        list (List[StarRailAchievementInfoList]): A list of achievement info objects.
    """

    achievement_num: int
    list: list[GenshinAchievementInfoList]
