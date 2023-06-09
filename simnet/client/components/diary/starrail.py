from typing import Optional

from simnet.client.components.diary.base import BaseDiaryClient
from simnet.models.starrail.diary import StarRailDiary
from simnet.utils.enum_ import Game


class StarrailDiaryClient(BaseDiaryClient):
    async def get_starrail_diary(
        self,
        player_id: Optional[int] = None,
        *,
        month: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailDiary:
        """Get a blazer's diary with earning details for the month."""
        data = await self.request_ledger(player_id, game=Game.STARRAIL, month=month, lang=lang)
        return StarRailDiary(**data)
