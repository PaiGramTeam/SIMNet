import asyncio
from typing import Optional, Any, List, Dict, Union
from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.client.routes import RECORD_URL
from simnet.errors import DataNotPublic, BadRequest
from simnet.models.genshin.chronicle.abyss import SpiralAbyss, SpiralAbyssPair
from simnet.models.genshin.chronicle.achievement import GenshinAchievementInfo
from simnet.models.genshin.chronicle.act_calendar import GenshinActCalendar
from simnet.models.genshin.chronicle.character_detail import GenshinCharacterListInfo, GenshinDetailCharacters
from simnet.models.genshin.chronicle.characters import Character
from simnet.models.genshin.chronicle.img_theater import ImgTheater
from simnet.models.genshin.chronicle.notes import Notes, NotesWidget, NotesOverseaWidget
from simnet.models.genshin.chronicle.stats import (
    PartialGenshinUserStats,
    GenshinUserStats,
    FullGenshinUserStats,
)
from simnet.models.lab.record import RecordCard
from simnet.utils.enums import Game, Region
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
        endpoint_type: str = "api",
        lang: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ):
        """Get an arbitrary object from StarRail's battle chronicle.

        Args:
            endpoint (str): The endpoint of the object to retrieve.
            endpoint_type (str, optional): The type of endpoint to send the request to.
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
            endpoint_type=endpoint_type,
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
        characters = await self.get_genshin_character_list(player_id, lang=lang)
        details = await self.get_genshin_character_detail([char.id for char in characters], player_id, lang=lang)
        data = []
        for d in details.characters:
            data.append(Character.from_detail(d))
        return data

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
        data = await self._request_genshin_record("index", player_id, lang=lang)
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

    async def get_genshin_imaginarium_theater(
        self,
        player_id: Optional[int] = None,
        need_detail: Optional[bool] = True,
        *,
        previous: bool = False,
        lang: Optional[str] = None,
    ) -> ImgTheater:
        """Get genshin imaginarium theater runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            need_detail (Optional[bool], optional): Whether to retrieve detailed data. Defaults to True.
            previous (bool, optional): Whether to retrieve the data for the previous season of the Imaginarium Theater.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            ImgTheater: genshin imaginarium theater runs.
        """
        payload = {
            "need_detail": need_detail,
            "schedule_type": 2 if previous else 1,
        }
        data = await self._request_genshin_record("role_combat", player_id, lang=lang, payload=payload)

        return ImgTheater(**data)

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
            Notes: The requested real-time notes.

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
            self._request_genshin_record("index", player_id, lang=lang),
            self.get_genshin_spiral_abyss(player_id, lang=lang, previous=False),
            self.get_genshin_spiral_abyss(player_id, lang=lang, previous=True),
            self.get_genshin_activities(player_id, lang=lang),
        )
        abyss = SpiralAbyssPair(current=abyss1, previous=abyss2)

        return FullGenshinUserStats(**user, abyss=abyss, activities=activities)

    async def get_genshin_activities(self, player_id: Optional[int] = None, *, lang: Optional[str] = None) -> Dict:
        """Get genshin activities.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            Dict: The requested get_genshin_activities.
        """
        return await self._request_genshin_record("activities", player_id, lang=lang)

    async def get_record_card(
        self,
        account_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> Optional[RecordCard]:
        """Get a genshin player record cards.

        Args:
            account_id: Optional[int], the user's account ID, defaults to None
            lang: Optional[str], the language version of the request, defaults to None

        Returns:
            Genshin player record cards.

        Returns:
            Optional[RecordCard]: RecordCard objects.
        """
        account_id = account_id or self.account_id

        record_cards = await self.get_record_cards(account_id, lang=lang)

        for record_card in record_cards:
            if record_card.game == Game.GENSHIN:
                return record_card

        return None

    async def get_genshin_notes_by_stoken(
        self,
        lang: Optional[str] = None,
    ) -> Union[NotesWidget, NotesOverseaWidget]:
        """Get Genshin's real-time notes.

        Args:
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            NotesWidget (Union[NotesWidget, NotesOverseaWidget]): The requested real-time notes.

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
        if self.region == Region.OVERSEAS:
            route = RECORD_URL.get_url(self.region, self.game) / "../community/apihub/api/widget/data"
            params = {"game_id": "2"}
            data = await self.request_lab(route, params=params, lang=lang)
            model = NotesOverseaWidget
        else:
            data = await self._request_genshin_record("widget/v2", endpoint_type="aapi", lang=lang)
            model = NotesWidget
        return model(**data)

    async def get_genshin_character_list(
        self,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> List[GenshinCharacterListInfo]:
        """Retrieve a list of Genshin Impact character information for a player.

        Args:
            player_id (Optional[int]): The ID of the player. Defaults to None.
            lang (Optional[str]): The language for the character information. Defaults to None.

        Returns:
            List[GenshinCharacterListInfo]: A list of GenshinCharacterListInfo objects containing character details.
        """

        data = await self._request_genshin_record("character/list", player_id, method="POST", lang=lang)
        return [GenshinCharacterListInfo(**i) for i in data["list"]]

    async def get_genshin_character_detail(
        self,
        characters: List[int],
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> GenshinDetailCharacters:
        """Retrieve detailed information about Genshin Impact characters.

        Args:
            characters (List[int]): The IDs of the characters to retrieve details for.
            player_id (Optional[int]): The ID of the player. Defaults to None.
            lang (Optional[str]): The language for the character information. Defaults to None.

        Returns:
            GenshinDetailCharacters: An object containing detailed information.
        """

        ids = [characters] if isinstance(characters, int) else characters
        payload = {"character_ids": ids}
        data = await self._request_genshin_record(
            "character/detail", player_id, method="POST", lang=lang, payload=payload
        )
        return GenshinDetailCharacters(**data)

    async def get_genshin_achievement_info(
        self, player_id: Optional[int] = None, *, lang: Optional[str] = None
    ) -> GenshinAchievementInfo:
        """Get genshin achievement info.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            GenshinAchievementInfo: The requested achievement info.
        """
        data = await self._request_genshin_record("achievement", player_id, method="POST", lang=lang)
        return GenshinAchievementInfo(**data)

    async def get_genshin_act_calendar(
        self, player_id: Optional[int] = None, *, lang: Optional[str] = None
    ) -> GenshinActCalendar:
        """Get genshin act calendar.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            GenshinActCalendar: The requested act calendar info.
        """
        data = await self._request_genshin_record("act_calendar", player_id, method="POST", lang=lang)
        return GenshinActCalendar(**data)
