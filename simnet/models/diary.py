from enum import IntEnum

from pydantic import Field

from simnet.models.base import APIModel

__all__ = (
    "DiaryType",
    "BaseDiary",
)


class DiaryType(IntEnum):
    """Type of diary pages."""

    PRIMOGEMS = 1
    """Primogems."""

    MORA = 2
    """Mora."""


class BaseDiary(APIModel):
    """Base model for diary and diary page."""

    uid: int
    server: str = Field(alias="region")
    nickname: str = ""
    month: int = Field(alias="data_month")
