from typing import Optional

from simnet.client.components.diary.base import BaseDiaryClient
from simnet.models.starrail.diary import StarRailDiary
from simnet.utils.enums import Game


class StarrailDiaryClient(BaseDiaryClient):
    """Starrail diary component."""

    async def get_starrail_diary(
        self,
        player_id: Optional[int] = None,
        *,
        month: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> StarRailDiary:
        """Get a traveler's diary with earning details for the month.

        Args:
            player_id (int, optional): The player's ID. Defaults to None.
            month (int, optional): The month to get the diary for. Defaults to None.
            lang (str, optional): The language to get the diary in. Defaults to None.

        Returns:
            Diary: The diary for the month.
        """
        data = await self.request_ledger(player_id, game=Game.STARRAIL, month=month, lang=lang)
        return StarRailDiary(**data)
