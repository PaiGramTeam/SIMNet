"""Starrail chronicle activity."""
from typing import List, Optional, Dict

from simnet.models.base import APIModel
from simnet.models.starrail.character import ActivityCharacter

from .base import PartialTime


class StarRailActivityBase(APIModel):
    """StarRailActivity Base Model"""

    exists_data: bool = True
    is_hot: bool
    strategy_link: str = ""


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


class StarRailTreasureDungeonRecord(APIModel):
    """Treasure Dungeon Record"""

    stage_id: int
    name: str
    difficulty_id: int
    avatars: List[ActivityCharacter]
    icon: str
    atk_buff: int
    def_buff: int
    used_stamina: int
    ancient_weapon: int
    ancient_armor: int
    ancient_bomb: int
    enemy_killed: int
    finish_time: Optional[PartialTime]
    special_buff: int

    @property
    def time_str(self) -> str:
        """Get the time as a string."""
        if self.finish_time is None:
            return "N/A"

        return self.finish_time.datetime.strftime("%Y.%m.%d %H:%M")


class StarRailTreasureDungeon(StarRailActivityBase):
    """Treasure Dungeon"""

    records: List[StarRailTreasureDungeonRecord]


class StarRailActivity(APIModel):
    """Starrail chronicle activity."""

    activities: List

    def find_activity(self, key: str) -> Optional[Dict]:
        """Find an activity by key."""
        for activity in self.activities:
            if list(activity.keys())[0] == key:
                return activity[key]
        raise ValueError("No starrail activity found.")

    @property
    def fantastic_story(self) -> StarRailFantasticStory:
        """Get the fantastic story activity."""
        return StarRailFantasticStory(**self.find_activity("fantastic_story"))

    @property
    def treasure_dungeon(self) -> StarRailTreasureDungeon:
        """Get the treasure dungeon activity."""
        return StarRailTreasureDungeon(**self.find_activity("treasure_dungeon"))
