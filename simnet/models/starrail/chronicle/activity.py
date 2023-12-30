"""Starrail chronicle activity."""
from typing import List, Optional, Dict

from simnet.models.base import APIModel
from simnet.models.starrail.character import ActivityCharacter, RogueCharacter

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


class StarRailYitaiBattleInfoBasic(APIModel):
    """Yitai Battle Info Basic"""

    gender: int
    rating_cur: int
    rating_id: int
    rating_max: int
    collect_cur: int
    collect_max: int
    rating_name: str


class StarRailYitaiBattleInfoFairyLandCity(APIModel):
    """Yitai Battle Info Fairy Land City"""

    id: int
    name: str
    has_challenge: bool
    stars_cur: int
    stars_max: int


class StarRailYitaiBattleInfoFairyLand(APIModel):
    """Yitai Battle Info Fairy Land"""

    is_open: bool
    kills: List[int]
    cities: List[StarRailYitaiBattleInfoFairyLandCity]


class StarRailYitaiBattleInfoLinkBattle(APIModel):
    """Yitai Battle Info Link Battle"""

    rank: int
    rank_name: str
    challenge_cur: int
    challenge_max: int


class StarRailYitaiBattleInfo(APIModel):
    """Yitai Battle Info"""

    basic: StarRailYitaiBattleInfoBasic
    fairy_land: StarRailYitaiBattleInfoFairyLand
    link_battle: List[StarRailYitaiBattleInfoLinkBattle]
    exists_data: bool = True


class StarRailYitaiBattleRecord(StarRailActivityBase):
    """Yitai Battle"""

    info: StarRailYitaiBattleInfo


class StarRailEndlessSideRecord(APIModel):
    """Endless Side Record"""

    name: str
    status: str
    level: int
    point: int
    avatars: List[ActivityCharacter]
    buff_cnt: int
    miracle_cnt: int
    base_buff_id: int
    base_buff_name: str
    rank: int
    cached_avatars: List[ActivityCharacter]

    @property
    def finished(self) -> bool:
        """Check if the record is finished."""
        return self.status == "PassHard"


class StarRailEndlessSideInfo(APIModel):
    """Endless Side Info"""

    total_score: str
    records: List[StarRailEndlessSideRecord]
    exists_data: bool = True


class StarRailEndlessSide(StarRailActivityBase):
    """Endless Side Activity"""

    info: StarRailEndlessSideInfo


class StarRailFoxStoryTeam(APIModel):
    """Fox Story Team"""

    level: int
    fans: int
    fans_range: List[int]
    phase: int

    @property
    def real_index_arrived(self) -> int:
        """Get the real index of the arrived fans."""
        for idx, num in enumerate(self.fans_range):
            if num >= self.fans:
                return idx
        return len(self.fans_range)

    @property
    def index_arrived(self) -> int:
        """Get the index of the arrived fans."""
        max_idx = len(self.fans_range) - 1
        return min(self.real_index_arrived, max_idx)

    @property
    def fans_str(self) -> str:
        """Get the fans as a string."""
        if self.fans < 10000:
            return str(self.fans)
        w = round(self.fans / 10000, 2)
        return f"{w}万"


class StarRailFoxStorySubdueDifficulty(APIModel):
    """Fox Story Subdue Difficulty"""

    has_challenge: bool
    star_cnt: int

    @property
    def stars(self) -> List[bool]:
        """Get the stars."""
        e = int(self.star_cnt)
        i = 0
        while e:
            e &= e - 1
            i += 1
        return [True] * i + [False] * (3 - i)

    @property
    def stars_sp(self) -> List[bool]:
        """Get the stars."""
        return [True] * self.star_cnt + [False] * (3 - self.star_cnt)


class StarRailFoxStorySubdue(APIModel):
    """Fox Story Subdue"""

    has_challenge: bool
    name_mi18n: str
    fire_cnt: int
    difficulties: List[StarRailFoxStorySubdueDifficulty]


class StarRailFoxStoryInfo(APIModel):
    """Fox Story Info"""

    team: StarRailFoxStoryTeam
    subdues: List[StarRailFoxStorySubdue]
    subdue_collect_cur: int
    subdue_collect_max: int
    exists_data: bool = True


class StarRailFoxStory(StarRailActivityBase):
    """Fox Story Activity"""

    info: StarRailFoxStoryInfo


class StarRailBoxingShowBuffsUsedActivity(APIModel):
    """Boxing Show Buffs Used Activity"""

    id: int
    name_mi18n: str
    desc_mi18n: str


class StarRailBoxingShowInfoItem(APIModel):
    """Boxing Show Info Item"""

    name_mi18n: str
    round: int
    is_perfect: bool
    has_challenge: bool
    challenge_id: int
    avatars_used_activity: List[RogueCharacter]
    buffs_used_activity: List[StarRailBoxingShowBuffsUsedActivity]

    @property
    def buffs(self) -> str:
        """Get the buffs as a string."""
        return "、".join([i.name_mi18n for i in self.buffs_used_activity])


class StarRailBoxingShowInfo(APIModel):
    """Boxing Show Info"""

    list: List[StarRailBoxingShowInfoItem]
    exists_data: bool = False


class StarRailBoxingShow(StarRailActivityBase):
    """Boxing Show Activity"""

    info: StarRailBoxingShowInfo


class StarRailSpaceZooFeature(APIModel):
    """Space Zoo Feature"""

    cur: int
    max: int
    channel: str
    name_mi18n: str


class StarRailSpaceZooInfo(APIModel):
    """Space Zoo Info"""

    cur_xyzw: int
    max_xyzw: int
    features: List[StarRailSpaceZooFeature]
    level: int


class StarRailSpaceZoo(StarRailActivityBase):
    """Space Zoo Activity"""

    info: StarRailSpaceZooInfo


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

    @property
    def yitai_battle(self) -> StarRailYitaiBattleRecord:
        """Get the yitai battle activity."""
        return StarRailYitaiBattleRecord(**self.find_activity("yitai_battle"))

    @property
    def endless_side(self) -> StarRailEndlessSide:
        """Get the endless side activity."""
        return StarRailEndlessSide(**self.find_activity("endless_side"))

    @property
    def fox_story(self) -> StarRailFoxStory:
        """Get the fox story activity."""
        return StarRailFoxStory(**self.find_activity("fox_story"))

    @property
    def boxing_show(self) -> StarRailBoxingShow:
        """Get the boxing show activity."""
        return StarRailBoxingShow(**self.find_activity("boxing_show"))

    @property
    def space_zoo(self) -> StarRailSpaceZoo:
        """Get the space zoo activity."""
        return StarRailSpaceZoo(**self.find_activity("space_zoo"))
