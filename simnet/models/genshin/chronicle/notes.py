from datetime import timedelta, datetime
from typing import Union, Literal, Tuple, List, Optional, Dict, Any

import pydantic


__all__ = ("Expedition", "ExpeditionCharacter", "Notes")

from pydantic import Field

from simnet.models.base import APIModel
from simnet.models.genshin.character import BaseCharacter


def _process_timedelta(time: Union[int, timedelta, datetime]) -> datetime:
    if isinstance(time, int):
        time = datetime.fromtimestamp(time).astimezone()

    if isinstance(time, timedelta):
        time = datetime.now().astimezone() + time

    if time < datetime(2000, 1, 1).astimezone():
        delta = timedelta(seconds=int(time.timestamp()))
        time = datetime.now().astimezone() + delta

    time = time.replace(second=0, microsecond=0)

    return time


class ExpeditionCharacter(BaseCharacter):
    """Expedition character."""


class Expedition(APIModel):
    """Real-Time note expedition."""

    character: ExpeditionCharacter = Field(alias="avatar_side_icon")
    status: Literal["Ongoing", "Finished"]
    remaining_time: timedelta = Field(alias="remained_time")

    @property
    def finished(self) -> bool:
        """Whether the expedition has finished."""
        return self.remaining_time <= timedelta(0)

    @property
    def completion_time(self) -> datetime:
        return datetime.now().astimezone() + self.remaining_time

    @pydantic.validator("character", pre=True)
    def __complete_character(cls, v: Any) -> Any:
        if isinstance(v, str):
            return dict(icon=v)  # type: ignore

        return v


class TransformerTimedelta(timedelta):
    """Transformer recovery time."""

    @property
    def timedata(self) -> Tuple[int, int, int, int]:
        seconds: int = super().seconds
        days: int = super().days
        hour, second = divmod(seconds, 3600)
        minute, second = divmod(second, 60)

        return days, hour, minute, second

    @property
    def hours(self) -> int:
        return self.timedata[1]

    @property
    def minutes(self) -> int:
        return self.timedata[2]

    @property
    def seconds(self) -> int:
        return self.timedata[3]


class Notes(APIModel):
    """Real-Time notes."""

    current_resin: int
    max_resin: int
    remaining_resin_recovery_time: timedelta = Field(alias="resin_recovery_time")

    current_realm_currency: int = Field(alias="current_home_coin")
    max_realm_currency: int = Field(alias="max_home_coin")
    remaining_realm_currency_recovery_time: timedelta = Field(
        alias="home_coin_recovery_time"
    )

    completed_commissions: int = Field(alias="finished_task_num")
    max_commissions: int = Field(alias="total_task_num")
    claimed_commission_reward: bool = Field(alias="is_extra_task_reward_received")

    remaining_resin_discounts: int = Field(alias="remain_resin_discount_num")
    max_resin_discounts: int = Field(alias="resin_discount_num_limit")

    remaining_transformer_recovery_time: Optional[TransformerTimedelta]

    expeditions: List[Expedition]
    max_expeditions: int = Field(alias="max_expedition_num")

    @property
    def resin_recovery_time(self) -> datetime:
        """The remaining time until resin recovery in seconds."""
        return datetime.now().astimezone() + self.remaining_resin_recovery_time

    @property
    def realm_currency_recovery_time(self) -> datetime:
        """The remaining time until realm currency recovery in seconds."""
        return datetime.now().astimezone() + self.remaining_realm_currency_recovery_time

    @property
    def transformer_recovery_time(self) -> Optional[datetime]:
        """The remaining time until realm currency recovery in seconds."""
        if self.remaining_transformer_recovery_time is None:
            return None

        remaining = (
            datetime.now().astimezone() + self.remaining_transformer_recovery_time
        )
        return remaining

    @pydantic.root_validator(pre=True)
    def __flatten_transformer(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "transformer_recovery_time" in values:
            return values

        if values.get("transformer") and values["transformer"]["obtained"]:
            t = values["transformer"]["recovery_time"]
            delta = TransformerTimedelta(
                days=t["Day"], hours=t["Hour"], minutes=t["Minute"], seconds=t["Second"]
            )
            values["remaining_transformer_recovery_time"] = delta
        else:
            values["remaining_transformer_recovery_time"] = None

        return values
