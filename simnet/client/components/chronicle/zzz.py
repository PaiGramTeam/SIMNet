from typing import Optional, Mapping, Dict, Any, List

from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.errors import BadRequest, DataNotPublic
from simnet.models.lab.record import RecordCard
from simnet.models.zzz.calculator import ZZZCalculatorCharacterDetails
from simnet.models.zzz.chronicle.notes import ZZZNote
from simnet.models.zzz.chronicle.stats import ZZZUserStats, ZZZAvatarBasic
from simnet.utils.enums import Game
from simnet.utils.player import recognize_region, recognize_zzz_server

__all__ = ("ZZZBattleChronicleClient",)


class ZZZBattleChronicleClient(BaseChronicleClient):
    """A client for retrieving data from ZZZ's battle chronicle component.

    This class is used to retrieve various data objects from StarRail's battle chronicle component,
    including real-time notes, user statistics, and character information.
    """

    async def _request_zzz_record(
        self,
        endpoint: str,
        player_id: Optional[int] = None,
        endpoint_type: str = "api",
        method: str = "GET",
        lang: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Mapping[str, Any]:
        """Get an arbitrary object from ZZZ's battle chronicle.

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
        payload = dict(role_id=player_id, server=recognize_zzz_server(player_id), **payload)

        data, params = None, None
        if method == "POST":
            data = payload
        else:
            params = payload

        return await self.request_game_record(
            endpoint,
            endpoint_type=endpoint_type,
            lang=lang,
            game=Game.ZZZ,
            region=recognize_region(player_id, game=Game.ZZZ),
            params=params,
            data=data,
        )

    async def get_zzz_notes(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
        autoauth: bool = True,
    ) -> ZZZNote:
        """Get ZZZ's real-time notes.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.
            autoauth (bool, optional): Whether to automatically authenticate the user. Defaults to True.

        Returns:
            ZZZNote: The requested real-time notes.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        try:
            data = await self._request_zzz_record("note", player_id, lang=lang)
        except DataNotPublic as e:
            # error raised only when real-time notes are not enabled
            if player_id and self.player_id != player_id:
                raise BadRequest(e.response, "Cannot view real-time notes of other users.") from e
            if not autoauth:
                raise BadRequest(e.response, "Real-time notes are not enabled.") from e
            await self.update_settings(3, True, game=Game.ZZZ)
            data = await self._request_zzz_record("note", player_id, lang=lang)

        return ZZZNote(**data)

    async def get_zzz_user(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> "ZZZUserStats":
        """Get ZZZ user statistics.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZUserStats: The requested user statistics.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_zzz_record("index", player_id, lang=lang)
        return ZZZUserStats(**data)

    async def get_zzz_characters(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> "ZZZAvatarBasic":
        """Get ZZZ character basic information.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZAvatarBasic: The requested character information.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_zzz_record("avatar/basic", player_id, lang=lang)
        return ZZZAvatarBasic(**data)

    async def get_zzz_character_info(
        self,
        characters: List[int],
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> "ZZZCalculatorCharacterDetails":
        """Get ZZZ character detail information.

        Args:
            characters (List[int]): A list of character IDs.
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZCalculatorCharacterDetails: The requested character information.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        ch = characters
        if isinstance(characters, int):
            ch = [characters]
        payload = {"need_wiki": "true", "id_list[]": ch}
        data = await self._request_zzz_record("avatar/info", player_id, lang=lang, payload=payload)
        return ZZZCalculatorCharacterDetails(**data)

    async def get_record_card(
        self,
        account_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> Optional[RecordCard]:
        """Get a zzz player record cards.

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
            if record_card.game == Game.ZZZ:
                return record_card

        return None
