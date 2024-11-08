import asyncio
from typing import Optional, Mapping, Dict, Any, Union, List

from simnet.client.components.chronicle.base import BaseChronicleClient
from simnet.client.routes import RECORD_URL
from simnet.errors import BadRequest, DataNotPublic
from simnet.models.lab.record import RecordCard
from simnet.models.starrail.chronicle.achievement import StarRailAchievementInfo
from simnet.models.starrail.chronicle.act_calendar import StarRailActCalendar
from simnet.models.starrail.chronicle.challenge import StarRailChallenge
from simnet.models.starrail.chronicle.challenge_boss import StarRailChallengeBoss
from simnet.models.starrail.chronicle.challenge_story import StarRailChallengeStory
from simnet.models.starrail.chronicle.characters import StarRailDetailCharacters
from simnet.models.starrail.chronicle.notes import StarRailNote, StarRailNoteWidget, StarRailNoteOverseaWidget
from simnet.models.starrail.chronicle.rogue import StarRailRogue, StarRailRogueLocust, StarRailRogueNous
from simnet.models.starrail.chronicle.rogue_tourn import StarRailRogueTourn
from simnet.models.starrail.chronicle.stats import StarRailUserStats, StarRailUserInfo
from simnet.models.starrail.diary import StarRailLedgerMonthInfo
from simnet.utils.enums import Game, Region
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
        endpoint_type: str = "api",
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
            endpoint_type=endpoint_type,
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

    async def get_starrail_challenge_story(
        self,
        player_id: Optional[int] = None,
        previous: bool = False,
        lang: Optional[str] = None,
    ) -> StarRailChallengeStory:
        """Get starrail challenge story runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            previous (bool, optional): Whether to get previous runs. Defaults to False.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailChallengeStory: The requested challenge story runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(schedule_type=2 if previous else 1, need_all="true", type="story")
        data = await self._request_starrail_record("challenge_story", player_id, lang=lang, payload=payload)
        return StarRailChallengeStory(**data)

    async def get_starrail_challenge_boss(
        self,
        player_id: Optional[int] = None,
        previous: bool = False,
        lang: Optional[str] = None,
    ) -> StarRailChallengeBoss:
        """Get starrail challenge boss runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            previous (bool, optional): Whether to get previous runs. Defaults to False.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailChallengeBoss: The requested challenge boss runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(schedule_type=2 if previous else 1, need_all="true", type="boss")
        data = await self._request_starrail_record("challenge_boss", player_id, lang=lang, payload=payload)
        return StarRailChallengeBoss(**data)

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

    async def get_starrail_rogue_locust(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailRogueLocust:
        """Get starrail rogue locust runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailRogueLocust: The requested rogue locust runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(need_detail="true")
        data = await self._request_starrail_record("rogue_locust", player_id, lang=lang, payload=payload)
        return StarRailRogueLocust(**data)

    async def get_starrail_rogue_nous(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailRogueNous:
        """Get starrail rogue nous runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailRogueNous: The requested rogue nous runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(need_detail="true")
        data = await self._request_starrail_record("rogue_nous", player_id, lang=lang, payload=payload)
        return StarRailRogueNous(**data)

    async def get_starrail_rogue_tourn(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailRogueTourn:
        """Get starrail rogue tourn runs.

        Args:
            player_id (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailRogueTourn: The requested rogue tourn runs.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        payload = dict(need_detail="true")
        data = await self._request_starrail_record("rogue_tourn", player_id, lang=lang, payload=payload)
        return StarRailRogueTourn(**data)

    async def get_starrail_act_calendar(
        self,
        uid: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailActCalendar:
        """Get starrail act calendar.

        Args:
            uid (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailActCalendar: The requested act calendar info.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_starrail_record("get_act_calender", uid, lang=lang)
        return StarRailActCalendar(**data)

    async def get_starrail_notes_by_stoken(
        self,
        lang: Optional[str] = None,
    ) -> Union[StarRailNoteWidget, StarRailNoteOverseaWidget]:
        """Get StarRail's real-time notes.

        Args:
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailNoteWidget (Union[StarRailNoteWidget, StarRailNoteOverseaWidget]): The requested real-time notes.

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
            route = RECORD_URL.get_url(self.region, self.game) / "../community/apihub/api/hsr_widget"
            data = await self.request_lab(route, lang=lang)
            model = StarRailNoteOverseaWidget
        else:
            data = await self._request_starrail_record("widget", endpoint_type="aapi", lang=lang)
            model = StarRailNoteWidget
        return model(**data)

    async def set_starrail_avatar_recommend_property(
        self,
        avatar_id: int,
        recommend_relic_properties: List[int] = None,
    ) -> None:
        """Set StarRail avatar recommend properties.

        Args:
            avatar_id (int): The avatar ID.
            recommend_relic_properties (List[int], optional): The recommend relic properties. Defaults to None.

        Raises:
            InternalDatabaseError: If the request is invalid.
        """
        payload = dict(
            avatar_id=avatar_id,
            recommend_relic_properties=recommend_relic_properties or [],
        )
        await self._request_starrail_record("setAvatarRecommendRelicProperty", method="POST", payload=payload)

    async def get_starrail_ledger_month_info(
        self,
        uid: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailLedgerMonthInfo:
        """Get StarRail ledger month info.

        Args:
            uid (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailLedgerMonthInfo: The requested activity info.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_starrail_record("get_ledger_month_info", uid, lang=lang)
        return StarRailLedgerMonthInfo(**data)

    async def get_starrail_achievement_info(
        self,
        uid: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarRailAchievementInfo:
        """Get StarRail achievement info.

        Args:
            uid (Optional[int], optional): The player ID. Defaults to None.
            lang (Optional[str], optional): The language of the data. Defaults to None.

        Returns:
            StarRailAchievementInfo: The requested achievement info.

        Raises:
            BadRequest: If the request is invalid.
            DataNotPublic: If the requested data is not public.
        """
        data = await self._request_starrail_record("achievement_info", uid, lang=lang)
        return StarRailAchievementInfo(**data)
