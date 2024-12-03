from collections.abc import Mapping
from typing import Any, Dict, List, Optional

from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.errors import BadRequest, DataNotPublic
from simnet.models.lab.record import RecordCard
from simnet.models.zzz.calculator import ZZZCalculatorCharacterDetails
from simnet.models.zzz.chronicle.abyss_abstract import ZZZAbyssAbstract
from simnet.models.zzz.chronicle.challenge import ZZZChallenge
from simnet.models.zzz.chronicle.notes import ZZZNote
from simnet.models.zzz.chronicle.stats import (
    ZZZAvatarBasic,
    ZZZBuddyBasic,
    ZZZUserStats,
)
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
        payload = dict(
            role_id=player_id, server=recognize_zzz_server(player_id), **payload
        )

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
                raise BadRequest(
                    e.response, "Cannot view real-time notes of other users."
                ) from e
            if not autoauth:
                raise BadRequest(e.response, "Real-time notes are not enabled.") from e
            await self.update_settings(3, True, game=Game.ZZZ)
            data = await self._request_zzz_record("note", player_id, lang=lang)

        return ZZZNote(**data)

    async def get_zzz_notes_by_stoken(
        self,
        lang: Optional[str] = None,
    ) -> ZZZNote:
        """Get zzz's real-time notes.

        Args:
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZNote (ZZZNote): The requested real-time notes.

        Raises:
            BadRequest: If the request is invalid.
        """
        stoken = self.cookies.get("stoken")
        if stoken is None:
            raise ValueError("stoken not found in cookies.")
        stuid = self.cookies.get("stuid")
        if stuid is None and self.account_id is None:
            raise ValueError("account_id or stuid not found")
        if self.account_id is not None and stuid is None:
            self.cookies.set("stuid", str(self.account_id))
        data = await self._request_zzz_record("widget", lang=lang)
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

    async def get_zzz_abyss_abstract(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> "ZZZAbyssAbstract":
        """Get ZZZ abyss abstract statistics.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZAbyssAbstract: The requested abyss abstract statistics.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_zzz_record("abyss_abstract", player_id, lang=lang)
        return ZZZAbyssAbstract(**data)

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
        data = await self._request_zzz_record(
            "avatar/info", player_id, lang=lang, payload=payload
        )
        return ZZZCalculatorCharacterDetails(**data)

    async def get_zzz_buddy_list(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> "ZZZBuddyBasic":
        """Get ZZZ buddy basic information.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZBuddyBasic: The requested buddy information.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_zzz_record("buddy/info", player_id, lang=lang)
        return ZZZBuddyBasic(**data)

    async def get_zzz_challenge(
        self,
        player_id: Optional[int] = None,
        previous: bool = False,
        lang: Optional[str] = None,
    ) -> ZZZChallenge:
        """Get zzz challenge runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            previous (bool, optional): Whether to get previous runs. Defaults to False.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ZZZChallenge: The requested challenge runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(schedule_type=2 if previous else 1, need_all="true")
        data = await self._request_zzz_record(
            "challenge", player_id, lang=lang, payload=payload
        )
        return ZZZChallenge(**data)

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
