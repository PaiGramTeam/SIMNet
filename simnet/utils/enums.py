import enum as _enum

__all__ = ("Region", "Game")


class Region(_enum.StrEnum):
    """
    Represents a region where a game is being played.

    Attributes:
        OVERSEAS (Region): Represents an overseas region where a game is being played.
        CHINESE (Region): Represents a Chinese region where a game is being played.
    """

    OVERSEAS = "os"
    CHINESE = "cn"


class Game(_enum.StrEnum):
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
