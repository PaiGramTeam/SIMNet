import asyncio
from typing import Optional, Mapping, Dict, Any

from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.errors import BadRequest, DataNotPublic
from simnet.models.lab.record import RecordCard
from simnet.models.starrail.chronicle.challenge import StarRailChallenge
from simnet.models.starrail.chronicle.characters import StarRailDetailCharacters
from simnet.models.starrail.chronicle.museum import StarRailMuseumBasic, StarRailMuseumDetail
from simnet.models.starrail.chronicle.notes import StarRailNote
from simnet.models.starrail.chronicle.rogue import StarRailRogue
from simnet.models.starrail.chronicle.stats import StarRailUserStats, StarRailUserInfo
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
            await self.update_settings(3, True, game=Game.STARRAIL)
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
        index_data, basic_info = await asyncio.gather(
            self._request_starrail_record("index", player_id, lang=lang),
            self._request_starrail_record("role/basicInfo", player_id, lang=lang),
        )
        basic_data = StarRailUserInfo(**basic_info)
        return StarRailUserStats(**index_data, info=basic_data)

    async def get_starrail_characters(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailDetailCharacters:
        """Get StarRail character information.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailDetailCharacters: The requested character information.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = {"need_wiki": "true"}
        data = await self._request_starrail_record("avatar/info", player_id, lang=lang, payload=payload)
        return StarRailDetailCharacters(**data)

    async def get_record_card(
        self,
        account_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> Optional[RecordCard]:
        """Get a starrail player record cards.

        Args:
            account_id: Optional[int], the user's account ID, defaults to None
            lang: Optional[str], the language version of the request, defaults to None

        Returns:
            Starrail user record cards.

        Returns:
            Optional[RecordCard]: RecordCard objects.
        """
        account_id = account_id or self.account_id

        record_cards = await self.get_record_cards(account_id, lang=lang)

        for record_card in record_cards:
            if record_card.game == Game.STARRAIL:
                return record_card

        return None

    async def get_starrail_challenge(
        self,
        player_id: Optional[int] = None,
        previous: bool = False,
        lang: Optional[str] = None,
    ) -> StarRailChallenge:
        """Get starrail challenge runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            previous (bool, optional): Whether to get previous runs. Defaults to False.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailChallenge: The requested challenge runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(schedule_type=2 if previous else 1, need_all="true")
        data = await self._request_starrail_record("challenge", player_id, lang=lang, payload=payload)
        return StarRailChallenge(**data)

    async def get_starrail_rogue(
        self,
        player_id: Optional[int] = None,
        schedule_type: int = 3,
        lang: Optional[str] = None,
    ) -> StarRailRogue:
        """Get starrail rogue runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            schedule_type (int, optional): The schedule type. Defaults to 3.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailRogue: The requested rogue runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(schedule_type=schedule_type, need_detail="true")
        data = await self._request_starrail_record("rogue", player_id, lang=lang, payload=payload)
        return StarRailRogue(**data)

    async def get_starrail_museum_info(
        self,
        uid: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailMuseumBasic:
        """Get starrail museum basic info.

        Args:
            uid (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailMuseumBasic: The requested museum basic info.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_starrail_record("museum/basic", uid, lang=lang)
        return StarRailMuseumBasic(**data)

    async def get_starrail_museum_detail(
        self,
        uid: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailMuseumDetail:
        """Get starrail museum detail info.

        Args:
            uid (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailMuseumDetail: The requested museum detail info.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_starrail_record("museum/detail", uid, lang=lang)
        return StarRailMuseumDetail(**data)
