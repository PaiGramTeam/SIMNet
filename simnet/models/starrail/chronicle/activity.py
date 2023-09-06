"""Starrail chronicle activity."""
from typing import List, Optional

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


class StarRailCopperManInfoBasic(APIModel):
    """Copper Man Info Basic"""

    level: int
    accumulate: int
    cur_common_order: int
    max_common_order: int
    cur_customer_order: int
    max_customer_order: int
    cur_alley_event: int
    max_alley_event: int

    @property
    def common_order_process(self) -> float:
        """Get the common order process."""
        return 100.0 * self.cur_common_order / self.max_common_order

    @property
    def customer_order_process(self) -> float:
        """Get the customer order process."""
        return 100.0 * self.cur_customer_order / self.max_customer_order

    @property
    def alley_event_process(self) -> float:
        """Get the alley event process."""
        return 100.0 * self.cur_alley_event / self.max_alley_event


class StarRailCopperManInfoShop(APIModel):
    """Copper Man Info Shop"""

    id: int
    icon: str
    name: str
    is_unlock: bool


class StarRailCopperManInfo(APIModel):
    """Copper Man Info"""

    basic: StarRailCopperManInfoBasic
    shops: List[StarRailCopperManInfoShop]
    exists_data: bool


class StarRailCopperMan(StarRailActivityBase):
    """Copper Man"""

    info: StarRailCopperManInfo


class StarRailActivity(APIModel):
    """Starrail chronicle activity."""

    activities: List

    def find_activity(self, key: str) -> Optional[dict]:
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

    @property
    def copper_man(self) -> StarRailCopperMan:
        """Get the copper man activity."""
        return StarRailCopperMan(**self.find_activity("copper_man"))
