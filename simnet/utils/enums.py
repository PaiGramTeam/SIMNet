import enum as _enum

__all__ = ("Region", "Game", "SocialPlatform")


class Region(str, _enum.Enum):
    """
    Represents a region where a game is being played.

    Attributes:
        OVERSEAS (Region): Represents an overseas region where a game is being played.
        CHINESE (Region): Represents a Chinese region where a game is being played.
    """

    OVERSEAS = "os"
    CHINESE = "cn"


class Game(str, _enum.Enum):
    """
    Represents a game that can be played in different regions.

    Attributes:
        GENSHIN (Game): Represents the game "Genshin Impact".
        HONKAI (Game): Represents the game "Honkai Impact 3rd".
        STARRAIL (Game): Represents the game "Honkai Impact 3rd RPG".
        ZZZ (Game): Represents the game "Zenless Zone Zero".
    """

    GENSHIN = "genshin"
    HONKAI = "honkai3rd"
    STARRAIL = "hkrpg"
    ZZZ = "nap"


class SocialPlatform(str, _enum.Enum):
    """
    Represents a social platform where a user can be registered.

    Attributes:
        BILIBILI (SocialPlatform): Represents the social platform "Bilibili".
        XIAOHONGSHU (SocialPlatform): Represents the social platform "Xiaohongshu".
        DOUYIN (SocialPlatform): Represents the social platform "Douyin".
        WECHAT (SocialPlatform): Represents the social platform "WeChat".
        QQ (SocialPlatform): Represents the social platform "QQ".
    """

    BILIBILI = "bilibili"
    XIAOHONGSHU = "xiaohongshu"
    DOUYIN = "douyin"
    WECHAT = "wechat"
    QQ = "qq"
