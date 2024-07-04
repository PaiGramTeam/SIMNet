"""Starrail base character model."""

from pydantic import Field

from simnet.models.base import APIModel


class ZZZBaseCharacter(APIModel):
    """Base character model."""

    id: int
    element_type: int
    rarity: str
    group_icon_path: str
    hollow_icon_path: str


class ZZZPartialCharacter(ZZZBaseCharacter):
    """Character without any equipment."""

    name: str = Field(alias="name_mi18n")
    full_name: str = Field(alias="full_name_mi18n")
    camp_name: str = Field(alias="camp_name_mi18n")
    avatar_profession: int
    level: int
    rank: int
