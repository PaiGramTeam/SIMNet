from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import Field

from simnet.models.base import APIModel

__all__ = ("BaseTransaction", "ItemTransaction", "Transaction", "TransactionKind")


class TransactionKind(str, Enum):
    """Possible kind of transaction.

    Attributes:
        PRIMOGEM: Primogem currency.
        CRYSTAL: Genesis crystal currency.
        RESIN: Resin currency.
        ARTIFACT: Artifact items from domains.
        WEAPON: Weapon items from domains and wishes.
    """

    PRIMOGEM = "primogem"
    CRYSTAL = "crystal"
    RESIN = "resin"
    ARTIFACT = "artifact"
    WEAPON = "weapon"


class BaseTransaction(APIModel):
    """Genshin transaction."""

    kind: TransactionKind

    id: int
    time: datetime = Field(alias="datetime")
    amount: int = Field(alias="add_num")
    reason: str


class Transaction(BaseTransaction):
    """Genshin transaction of currency."""

    kind: Literal[TransactionKind.PRIMOGEM, TransactionKind.CRYSTAL, TransactionKind.RESIN]


class ItemTransaction(BaseTransaction):
    """Genshin transaction of artifacts or weapons."""

    kind: Literal[TransactionKind.ARTIFACT, TransactionKind.WEAPON]

    name: str
    rarity: int = Field(alias="quality")
