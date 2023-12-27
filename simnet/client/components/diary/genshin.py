from typing import Optional

from simnet.client.components.diary.base import BaseDiaryClient
from simnet.models.genshin.diary import Diary
from simnet.utils.enums import Game


class GenshinDiaryClient(BaseDiaryClient):
    """Genshin diary component."""

    async def get_genshin_diary(
        self,
        player_id: Optional[int] = None,
        *,
        month: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> Diary:
        """Get a traveler's diary with earning details for the month.

        Args:
            player_id (int, optional): The player's ID. Defaults to None.
            month (int, optional): The month to get the diary for. Defaults to None.
            lang (str, optional): The language to get the diary in. Defaults to None.

        Returns:
            Diary: The diary for the month.
        """
        data = await self.request_ledger(player_id, game=Game.GENSHIN, month=month, lang=lang)
        return Diary(**data)
