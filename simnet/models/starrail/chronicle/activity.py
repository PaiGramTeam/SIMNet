"""Starrail chronicle activity."""
from typing import List, Optional

from simnet.models.base import APIModel
from simnet.models.starrail.character import ActivityCharacter

from .base import PartialTime

__all__ = ["StarRailActivityBase", "StarRailStarFightRecord", "StarRailStarFight", "StarRailActivity"]


class StarRailActivityBase(APIModel):
    """StarRailActivity Base Model"""

    exists_data: bool
    is_hot: bool
    strategy_link: str = ""


class StarRailStarFightRecord(APIModel):
    """Stellar Flare Record"""

    name: str
    difficulty_id: int
    round: int
    stage_id: int
    time: Optional[PartialTime]
    lineup: List[ActivityCharacter]

    @property
    def time_str(self) -> str:
        """Get the time as a string."""
        if self.time is None:
            return "N/A"

        return self.time.datetime.strftime("%Y.%m.%d %H:%M")


class StarRailStarFight(StarRailActivityBase):
    """Stellar Flare"""

    records: List[StarRailStarFightRecord]


class StarRailFantasticStoryBuff(APIModel):
    """Fantastic Story Buff"""

    id: int
    name: str
    desc: str
    icon: str


class StarRailFantasticStoryRecord(APIModel):
    """Fantastic Story Record"""

    name: str
    score: int
    score_rank: int
    stage_id: int
    finish_time: Optional[PartialTime]
    avatars: List[ActivityCharacter]
    buffs: List[StarRailFantasticStoryBuff]

    @property
    def time_str(self) -> str:
        """Get the time as a string."""
        if self.finish_time is None:
            return "N/A"

        return self.finish_time.datetime.strftime("%Y.%m.%d %H:%M")


class StarRailFantasticStory(StarRailActivityBase):
    """Fantastic Story"""

    records: List[StarRailFantasticStoryRecord]


class StarRailActivity(APIModel):
    """Starrail chronicle activity."""

    activities: List

    def find_activity(self, key: str) -> Optional[dict]:
        """Find an activity by key."""
        for activity in self.activities:
            if list(activity.keys())[0] == key:
                return activity

        return None

    @property
    def star_fight(self) -> StarRailStarFight:
        """Get the star fight activity."""
        if data := self.find_activity("star_fight"):
            return StarRailStarFight(**data["star_fight"])

        raise ValueError("No star fight activity found.")

    @property
    def fantastic_story(self) -> StarRailFantasticStory:
        """Get the fantastic story activity."""
        if data := self.find_activity("fantastic_story"):
            return StarRailFantasticStory(**data["fantastic_story"])

        raise ValueError("No fantastic story activity found.")
