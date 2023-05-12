from typing import Optional, Mapping, Dict, Any

from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.errors import BadRequest, DataNotPublic
from simnet.models.starrail.chronicle.characters import StarShipDetailCharacters
from simnet.models.starrail.chronicle.notes import StarRailNote
from simnet.models.starrail.chronicle.stats import StarRailUserStats
from simnet.utils.enum_ import Game
from simnet.utils.player import recognize_starrail_server, recognize_region

__all__ = ("StarRailBattleChronicleClient",)


class StarRailBattleChronicleClient(BaseChronicleClient):
    """A client for retrieving data from StarRail's battle chronicle component.

    This class is used to retrieve various data objects from StarRail's battle chronicle component,
    including real-time notes, user statistics, and character information.
    """

    async def _request_starrail_record(
        self,
        endpoint: str,
        player_id: Optional[int] = None,
        method: str = "GET",
        lang: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Mapping[str, Any]:
        """Get an arbitrary object from StarRail's battle chronicle.

        Args:
            endpoint (str): The endpoint of the object to retrieve.
            player_id (Optional[int], optional): The player ID. Defaults to None.
            method (str, optional): The HTTP method to use. Defaults to "GET".
            lang (Optional[str], optional): The language of the data. Defaults to None.
            payload (Optional[Dict[str, Any]], optional): The request payload. Defaults to None.

        Returns:
            Mapping[str, Any]: The requested object.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(payload or {})

        player_id = player_id or self.player_id
        payload = dict(role_id=player_id, server=recognize_starrail_server(player_id), **payload)

        data, params = None, None
        if method == "POST":
            data = payload
        else:
            params = payload

        return await self.request_game_record(
            endpoint,
            lang=lang,
            game=Game.STARRAIL,
            region=recognize_region(player_id, game=Game.STARRAIL),
            params=params,
            data=data,
        )

    async def get_starrail_notes(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
        autoauth: bool = True,
    ) -> StarRailNote:
        """Get StarRail's real-time notes.

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
            data = await self._request_starrail_record("note", player_id, lang=lang)
        except DataNotPublic as e:
            # error raised only when real-time notes are not enabled
            if player_id and self.player_id != player_id:
                raise BadRequest(e.response, "Cannot view real-time notes of other users.") from e
            if not autoauth:
                raise BadRequest(e.response, "Real-time notes are not enabled.") from e
            data = await self._request_starrail_record("note", player_id, lang=lang)

        return StarRailNote(**data)

    async def get_starrail_user(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> StarRailUserStats:
        """Get StarRail user statistics.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailUserStats: The requested user statistics.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_starrail_record("index", player_id, lang=lang)
        return StarRailUserStats(**data)

    async def get_starrail_characters(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarShipDetailCharacters:
        """Get StarRail character information.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarShipDetailCharacters: The requested character information.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = {"need_wiki": "true"}
        data = await self._request_starrail_record("avatar/info", player_id, lang=lang, payload=payload)
        return StarShipDetailCharacters(**data)
