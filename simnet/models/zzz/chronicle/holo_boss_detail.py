from simnet.models.base import APIModel, TimeDeltaField
from simnet.models.starrail.chronicle.base import PartialTime
from simnet.models.zzz.chronicle.challenge import ZZZChallengeCharacter


class ZZZHoloBossDetailBossMedal(APIModel):
    """Medal awarded for defeating a boss in the Hollow boss challenge.

    Attributes:
        medal_icon: The icon URL of the medal.
        medal_id: The unique identifier of the medal.
        is_no_injured: Whether the medal was earned without the party taking
            any damage during the challenge.
    """

    medal_icon: str
    medal_id: int
    is_no_injured: bool


class ZZZHoloBossDetailBoss(APIModel):
    """Boss encountered in the Hollow boss challenge.

    Attributes:
        icon: The icon URL of the boss.
        name: The display name of the boss.
        medal: The medal awarded for defeating this boss.
    """

    icon: str
    name: str
    medal: ZZZHoloBossDetailBossMedal


class ZZZHoloBossDetailData(APIModel):
    """Detailed record of a single Hollow boss challenge attempt.

    Attributes:
        rank: The ranking of the attempt.
        star: The star rating of the attempt.
        challenge_time: The timestamp at which the challenge was completed,
            or ``None`` if not yet recorded.
        boss: The boss that was challenged.
        avatar_list: The list of characters used in the challenge attempt.
    """

    rank: int
    star: int
    challenge_time: PartialTime | None = None
    boss: ZZZHoloBossDetailBoss
    avatar_list: list[ZZZChallengeCharacter]


class ZZZHoloBossDetail(APIModel):
    """Full Hollow boss challenge details for a given period.

    Attributes:
        start_time: The start timestamp of the challenge period.
        end_time: The end timestamp of the challenge period.
        list: The list of challenge attempt records within this period.
        unlock: Whether the Hollow boss challenge is unlocked for the user.
        refresh_time: The remaining time until the challenge data refreshes.
    """

    start_time: PartialTime
    end_time: PartialTime
    list: list[ZZZHoloBossDetailData]
    unlock: bool
    refresh_time: TimeDeltaField

    @property
    def season(self) -> int:
        return int(f"{self.start_time.year}{self.start_time.month:02}")

    @property
    def total_star(self) -> int:
        return sum([i.star for i in self.list if i])

    @property
    def has_data(self) -> bool:
        if not self.unlock:
            return False
        avatars = []
        for i in self.list:
            avatars.extend(i.avatar_list)
        return bool(avatars)
