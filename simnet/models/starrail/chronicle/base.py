"""Starrail Chronicle Base Model."""
import datetime
from typing import Optional

from simnet.models.base import APIModel


class PartialTime(APIModel):
    """Partial time model."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: Optional[int] = None

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second or 0)
