import asyncio
from typing import Optional, Any, List, Dict

from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.errors import DataNotPublic, BadRequest
from simnet.models.genshin.chronicle.abyss import SpiralAbyss, SpiralAbyssPair
from simnet.models.genshin.chronicle.characters import Character
from simnet.models.genshin.chronicle.notes import Notes
from simnet.models.genshin.chronicle.stats import (
    PartialGenshinUserStats,
    GenshinUserStats,
    FullGenshinUserStats,
)
from simnet.utils.enum_ import Game
from simnet.utils.player import recognize_genshin_server, recognize_region

__all__ = ("GenshinBattleChronicleClient",)


class GenshinBattleChronicleClient(BaseChronicleClient):
    """A client for retrieving data from Genshin's battle chronicle component.

    This class is used to retrieve various data objects from StarRail's battle chronicle component,
    including real-time notes, user statistics, and character information.
    """

    async def _request_genshin_record(
        self,
        endpoint: str,
        player_id: Optional[int] = None,
        method: str = "GET",
        lang: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ):
        """Get an arbitrary object from StarRail's battle chronicle.

        Args:
            endpoint (str): The endpoint of the object to retrieve.
            player_id (Optional[int], optional): The player ID. Defaults to None.
            method (str, optional): The HTTP method to use. Defaults to "GET".
            lang (Optional[str], optional): The language of the data. Defaults to None.
            payload (Optional[Dict[str, Any]], optional): The request payload. Defaults to None.

        Returns:
            Dict[str, Any]: The requested object.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
            ValueError: If the player ID is not specified.
        """
        player_id = player_id or self.player_id

        if player_id is None:
            raise ValueError("Player ID is not specified.")

        if payload is None:
            payload = dict(role_id=player_id, server=recognize_genshin_server(player_id))
        else:
            payload = dict(role_id=player_id, server=recognize_genshin_server(player_id), **payload)

        data, params = None, None
        if method == "POST":
            data = payload
        else:
            params = payload

        return await self.request_game_record(
            endpoint,
            lang=lang,
            game=Game.GENSHIN,
            region=recognize_region(player_id, game=Game.GENSHIN),
            params=params,
            data=data,
        )

    async def get_partial_genshin_user(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> PartialGenshinUserStats:
        """Get partial genshin user without character equipment.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            PartialGenshinUserStats: The requested partial genshin user without character equipment.
        """
        data = await self._request_genshin_record("index", player_id, lang=lang)
        return PartialGenshinUserStats(**data)

    async def get_genshin_characters(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> List[Character]:
        """Get genshin user characters.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            Character: The requested genshin user characters.
        """
        data = await self._request_genshin_record("character", player_id, lang=lang, method="POST")
        return [Character(**i) for i in data["avatars"]]

    async def get_genshin_user(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> GenshinUserStats:
        """Get genshin user stats.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            GenshinUserStats: The requested genshin user stats.
        """
        data, character_data = await asyncio.gather(
            self._request_genshin_record("index", player_id, lang=lang),
            self._request_genshin_record("character", player_id, lang=lang, method="POST"),
        )
        data = {**data, **character_data}

        return GenshinUserStats(**data)

    async def get_genshin_spiral_abyss(
        self,
        player_id: Optional[int] = None,
        *,
        previous: bool = False,
        lang: Optional[str] = None,
    ) -> SpiralAbyss:
        """Get genshin spiral abyss runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            previous (bool, optional): Whether to retrieve the data for the previous season of the Spiral Abyss.
                Defaults to False.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            SpiralAbyss: genshin spiral abyss runs.
        """
        payload = dict(schedule_type=2 if previous else 1)
        data = await self._request_genshin_record("spiralAbyss", player_id, lang=lang, payload=payload)

        return SpiralAbyss(**data)

    async def get_genshin_notes(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
        autoauth: bool = True,
    ) -> Notes:
        """Get Genshin's real-time notes.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.
            autoauth (bool, optional): Whether to automatically authenticate the user. Defaults to True.

        Returns:
            StarRailNote: The requested real-time notes.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        try:
            data = await self._request_genshin_record("dailyNote", player_id, lang=lang)
        except DataNotPublic as e:
            # error raised only when real-time notes are not enabled
            if player_id and self.player_id != player_id:
                raise BadRequest(e.response, "Cannot view real-time notes of other users.") from e
            if not autoauth:
                raise BadRequest(e.response, "Real-time notes are not enabled.") from e

            await self.update_settings(3, True, game=Game.GENSHIN)
            data = await self._request_genshin_record("dailyNote", lang=lang)

        return Notes(**data)

    async def get_full_genshin_user(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> FullGenshinUserStats:
        """Get a genshin user with all their possible data.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            Character: The requested genshin user with all their possible data.
        """
        user, abyss1, abyss2, activities = await asyncio.gather(
            self.get_genshin_user(player_id, lang=lang),
            self.get_genshin_spiral_abyss(player_id, lang=lang, previous=False),
            self.get_genshin_spiral_abyss(player_id, lang=lang, previous=True),
            self.get_genshin_activities(player_id, lang=lang),
        )
        abyss = SpiralAbyssPair(current=abyss1, previous=abyss2)

        return FullGenshinUserStats(**user.dict(), abyss=abyss, activities=activities)

    async def get_genshin_activities(self, player_id: Optional[int] = None, *, lang: Optional[str] = None) -> Dict:
        """Get genshin activities.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            Dict: The requested get_genshin_activities.
        """
        return await self._request_genshin_record("activities", player_id, lang=lang)
