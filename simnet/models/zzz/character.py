"""Starrail base character model."""

from pydantic import Field

from simnet.models.base import APIModel


class ZZZBaseCharacter(APIModel):
    """Base character model."""

    id: int
    element_type: int
    rarity: str

    @property
    def icon(self) -> str:
        return (
            f"https://act-webstatic.hoyoverse.com/game_record/zzz/role_square_avatar/role_square_avatar_{self.id}.png"
        )


class ZZZPartialCharacter(ZZZBaseCharacter):
    """Character without any equipment."""

    name: str = Field(alias="name_mi18n")
    full_name: str = Field(alias="full_name_mi18n")
    camp_name: str = Field(alias="camp_name_mi18n")
    avatar_profession: int
    level: int
    rank: int
    group_icon_path: str
    hollow_icon_path: str


class ZZZBaseBuddy(APIModel):
    """Base Buddy model."""

    id: int
    rarity: str
    level: int

    @property
    def icon(self) -> str:
        return f"https://act-webstatic.hoyoverse.com/game_record/zzz/bangboo_square_avatar/bangboo_square_avatar_{self.id}.png"


class ZZZPartialBuddy(ZZZBaseBuddy):
    """Buddy"""

    name: str
    star: int
