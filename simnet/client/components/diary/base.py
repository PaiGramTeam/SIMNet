from datetime import timedelta, timezone, datetime
from typing import Optional, Any, Dict, Union

from simnet.client.base import BaseClient
from simnet.client.routes import DETAIL_LEDGER_URL, INFO_LEDGER_URL
from simnet.models.diary import DiaryType
from simnet.models.genshin.diary import DiaryPage
from simnet.utils.enums import Region, Game
from simnet.utils.player import recognize_server

__all__ = ("BaseDiaryClient",)

CN_TIMEZONE = timezone(timedelta(hours=8))


class BaseDiaryClient(BaseClient):
    """Base diary component."""

    async def request_ledger(
        self,
        player_id: Optional[int] = None,
        *,
        game: Optional[Game] = None,
        detail: bool = False,
        month: Union[int, str, None] = None,
        lang: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request towards the ys ledger endpoint.

        Args:
            player_id (Optional[int], optional): The player ID to get the ledger for.
            game (Optional[Game], optional): The game to get the ledger for.
            detail (bool, optional): Whether to get the detailed ledger.
            month (Optional[int], optional): The month to get the ledger for.
            lang (Optional[str], optional): The language code to use for the request.
            params (Optional[Dict[str, Any]], optional): The query parameters to use for the request.

        Returns:
            Dict[str, Any]: The response data.
        """
        game = game or self.game
        player_id = player_id or self.player_id
        params = params or {}

        base_url = DETAIL_LEDGER_URL if detail else INFO_LEDGER_URL
        url = base_url.get_url(self.region, game)

        if self.region == Region.OVERSEAS or game == Game.STARRAIL:
            params["uid"] = player_id
            params["region"] = recognize_server(player_id, game)
        elif self.region == Region.CHINESE:
            params["bind_uid"] = player_id
            params["bind_region"] = recognize_server(player_id, game)
        else:
            raise TypeError(f"{self.region!r} is not a valid region.")
        if game == Game.STARRAIL:
            month = month or datetime.now(CN_TIMEZONE).strftime("%Y%m")
        elif game == Game.GENSHIN:
            month = month or str(datetime.now(CN_TIMEZONE).month)
        params["month"] = month
        params["lang"] = lang or self.lang

        return await self.request_lab(url, params=params)

    async def _get_diary_page(
        self,
        page: int,
        *,
        game: Optional[Game] = None,
        player_id: Optional[int] = None,
        diary_type: int = DiaryType.PRIMOGEMS,
        month: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> DiaryPage:
        """Get a diary page.

        Args:
            page (int): The page number to get.
            game (Optional[Game], optional): The game to get the diary page for.
            player_id (Optional[int], optional): The player ID to get the diary page for.
            diary_type (int, optional): The diary type to get the diary page for.
            month (Optional[int], optional): The month to get the diary page for.
            lang (Optional[str], optional): The language code to use for the request.

        Returns:
            DiaryPage: The diary page.
        """
        data = await self.request_ledger(
            player_id,
            game=game,
            detail=True,
            month=month,
            lang=lang,
            params=dict(type=diary_type, current_page=page, page_size=100),
        )
        return DiaryPage(**data)
