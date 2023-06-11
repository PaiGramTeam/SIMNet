"""Starrail Museum models."""
from typing import List

from simnet.models.base import APIModel


class StarRailMuseumBasic(APIModel):
    """Starrail Museum basic info."""

    current_exp: int
    max_exp: int
    exhibition_num: int
    total_exhibition: int
    director_num: int
    total_director: int
    phase: str

    @property
    def progress_exp(self) -> float:
        """Get progress exp."""
        return self.current_exp / self.max_exp

    @property
    def progress_exhibition(self) -> float:
        """Get progress exhibition."""
        return self.exhibition_num / self.total_exhibition

    @property
    def progress_director(self) -> float:
        """Get progress director."""
        return self.director_num / self.total_director


class StarRailMuseumExhibition(APIModel):
    """Starrail Museum exhibition info."""

    id: str
    name: str
    desc: str
    is_unlock: bool
    icon: str


class StarRailMuseumRegion(APIModel):
    """Starrail Museum region info."""

    name: str
    exhibition_num: int
    total_exhibition: int
    exhibitions: List[StarRailMuseumExhibition]
    icon: str


class StarRailMuseumDirector(APIModel):
    """Starrail Museum director info."""

    id: str
    name: str
    desc: str
    is_unlock: bool
    icon: str


class StarRailMuseumDetail(APIModel):
    """Starrail Museum detail info."""

    regions: List[StarRailMuseumRegion]
    director: List[StarRailMuseumDirector]
    exhibition_more: str
    director_more: str
