from datetime import timedelta, timezone, datetime
from typing import Optional, Any, Dict

from simnet.client.base import BaseClient
from simnet.client.routes import DETAIL_LEDGER_URL, INFO_LEDGER_URL
from simnet.models.diary import DiaryType
from simnet.models.genshin.diary import DiaryPage
from simnet.utils.enum_ import Region, Game
from simnet.utils.player import recognize_server

__all__ = ("BaseDiaryClient",)

CN_TIMEZONE = timezone(timedelta(hours=8))


class BaseDiaryClient(BaseClient):
    """Diary component."""

    async def request_ledger(
        self,
        player_id: Optional[int] = None,
        *,
        game: Optional[Game] = None,
        detail: bool = False,
        month: Optional[int] = None,
        lang: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make a request towards the ys ledger endpoint."""
        url = (
            DETAIL_LEDGER_URL.get_url(self.region)
            if detail
            else INFO_LEDGER_URL.get_url(
                self.region,
                game,
            )
        )

        if self.region == Region.OVERSEAS or game == Game.STARRAIL:
            params["player_id"] = player_id
            params["region"] = recognize_server(player_id, game)
        elif self.region == Region.CHINESE:
            params["bind_uid"] = player_id
            params["bind_region"] = recognize_server(player_id, game)
        else:
            raise TypeError(f"{self.region!r} is not a valid region.")
        params["month"] = month or (datetime.now().strftime("%Y%m") if game == Game.STARRAIL else datetime.now().month)
        params["lang"] = lang or self.lang

        return await self.request_lab(url, params=params, **kwargs)

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
        data = await self.request_ledger(
            player_id,
            game=game,
            detail=True,
            month=month,
            lang=lang,
            params=dict(type=diary_type, current_page=page, page_size=100),
        )
        return DiaryPage(**data)
