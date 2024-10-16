from typing import Dict

from simnet.models.base import APIModel


class AccompanyRole(APIModel):
    """
    Represents the role of an accompany in the system.

    Attributes:
        accompany_days (int): The number of days the accompany role has been active.
        accompany_quarter_days (int): The number of quarter days the accompany role has been active.
        increase_accompany_point (int): The points increased by the accompany role.
    """

    accompany_days: int
    accompany_quarter_days: int
    increase_accompany_point: int


class AccompanyInfo(APIModel):
    """
    Represents the information related to an accompany role.

    Attributes:
        accompany_days (int): The number of days the accompany role has been active.
        accompany_quarter_days (int): The number of quarter days the accompany role has been active.
        accompany_point (int): The total points accumulated by the accompany role.
        available_accompany_point (int): The available points that can be used by the accompany role.
        is_accompany_today (bool): Indicates whether the accompany role is active today.
        can_accompany (bool): Indicates whether the accompany role can be active.
        accompany_upgrade_switch (bool): Indicates whether the accompany role upgrade is enabled.
    """

    accompany_days: int
    accompany_quarter_days: int
    accompany_point: int
    available_accompany_point: int

    is_accompany_today: bool
    can_accompany: bool

    accompany_upgrade_switch: bool


class TargetUserInfo(APIModel):
    """
    Represents the target user's information.

    Attributes:
        nickname (str): The nickname of the target user.
        avatar_url (str): The URL of the target user's avatar.
        is_following (bool): Indicates whether the current user is following the target user.
    """

    nickname: str
    avatar_url: str
    is_following: bool


class AccompanyRoleInfo(APIModel):
    """
    Represents the information related to an accompany role and the target user.

    Attributes:
        accompany_info (AccompanyInfo): The information related to the accompany role.
        target_user_info (TargetUserInfo): The information related to the target user.
    """

    accompany_info: AccompanyInfo
    target_user_info: TargetUserInfo


class AccompanyRoleBasic(APIModel):
    """
    Represents the basic information of an accompany role.

    Attributes:
        name (str): The name of the accompany role.
        role_id (int): The unique identifier for the accompany role.
        topic_id (int): The unique identifier for the topic associated with the accompany role.
        is_birthday (bool): Indicates whether it is the birthday of the accompany role.
        game_name (str): The name of the game associated with the accompany role.
        game_id (int): The unique identifier for the game associated with the accompany role.
        brief_name (str): A brief name or alias for the accompany role.
        attr (Dict): Additional attributes related to the accompany role.
    """

    name: str
    role_id: int
    topic_id: int

    is_birthday: bool
    game_name: str
    game_id: int
    brief_name: str

    attr: Dict
