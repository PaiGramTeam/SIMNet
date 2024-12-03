from typing import Optional

from simnet.client.components.diary.base import BaseDiaryClient
from simnet.models.zzz.diary import ZZZDiary
from simnet.utils.enums import Game


class ZZZDiaryClient(BaseDiaryClient):
    """ZZZ diary component."""

    async def get_zzz_diary(
        self,
        player_id: Optional[int] = None,
        *,
        month: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> ZZZDiary:
        """Get a traveler's diary with earning details for the month.

        Args:
            player_id (int, optional): The player's ID. Defaults to None.
            month (int, optional): The month to get the diary for. Defaults to None.
            lang (str, optional): The language to get the diary in. Defaults to None.

        Returns:
            ZZZDiary: The diary for the month.
        """
        data = await self.request_ledger(
            player_id, game=Game.ZZZ, month=month, lang=lang
        )
        return ZZZDiary(**data)
