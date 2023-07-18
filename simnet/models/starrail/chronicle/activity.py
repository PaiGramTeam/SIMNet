"""Starrail chronicle activity."""
from typing import List, Optional

from simnet.models.base import APIModel
from simnet.models.starrail.character import StarFightCharacter

from .base import PartialTime

__all__ = ["StarRailActivityBase", "StarRailStarFightRecord", "StarRailStarFight", "StarRailActivity"]


class StarRailActivityBase(APIModel):
    """ StarRailActivity Base Model """

    exists_data: bool
    is_hot: bool
    strategy_link: str = ""


class StarRailStarFightRecord(APIModel):
    """ Stellar Flare Record """

    name: str
    difficulty_id: int
    round: int
    stage_id: int
    time: Optional[PartialTime]
    lineup: List[StarFightCharacter]

    @property
    def time_str(self) -> str:
        """Get the time as a string."""
        if self.time is None:
            return "N/A"

        return self.time.datetime.strftime("%Y.%m.%d %H:%M")


class StarRailStarFight(StarRailActivityBase):
    """ Stellar Flare """

    records: List[StarRailStarFightRecord]


class StarRailActivity(APIModel):
    """Starrail chronicle activity."""

    activities: List

    @property
    def star_fight(self) -> StarRailStarFight:
        """Get the star fight activity."""
        for activity in self.activities:
            if list(activity.keys())[0] == "star_fight":
                return StarRailStarFight(**activity["star_fight"])

        raise ValueError("No star fight activity found.")
