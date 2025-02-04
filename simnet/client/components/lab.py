import asyncio
from typing import Any, Optional

from simnet.client.base import BaseClient
from simnet.client.headers import Headers
from simnet.client.routes import (
    BBS_URL,
    CODE_HOYOLAB_URL,
    CODE_URL,
    HK4E_URL,
    TAKUMI_URL,
)
from simnet.models.lab.accompany import (
    AccompanyRole,
    AccompanyRoleBasic,
    AccompanyRoleInfo,
)
from simnet.models.lab.announcement import Announcement
from simnet.models.lab.record import Account, FullUser, PartialUser
from simnet.utils.enums import Game, Region
from simnet.utils.lang import create_short_lang_code
from simnet.utils.player import (
    recognize_game_biz,
    recognize_genshin_server,
    recognize_server,
)
from simnet.utils.types import HeaderTypes

__all__ = ("LabClient",)


class LabClient(BaseClient):
    """LabClient component."""

    async def request_bbs(
        self,
        endpoint: str,
        *,
        lang: Optional[str] = None,
        region: Optional[Region] = None,
        method: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[HeaderTypes] = None,
    ) -> dict[str, Any]:
        """Makes a request to a bbs endpoint.

        Args:
            endpoint (str): The URL of the endpoint to make the request to.
            lang (str, optional): The language code used for the request. Defaults to None.
            region (Region, optional): The server region used for the request. Defaults to None.
            method (str, optional): The HTTP method used for the request. Defaults to None.
            params (dict, optional): The parameters to include in the request. Defaults to None.
            data (any, optional): The data to include in the request. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            Dict[str, Any]: The response data from the request.
        """
        headers = Headers(headers)

        lang = lang or self.lang
        region = region or self.region

        url = BBS_URL.get_url(region) / endpoint

        if self.region == Region.CHINESE:
            headers["Referer"] = "https://www.miyoushe.com/"

        return await self.request_lab(
            url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            lang=lang,
            new_ds=self.region == Region.CHINESE,
        )

    async def search_users(
        self,
        keyword: str,
        *,
        lang: Optional[str] = None,
    ) -> list[PartialUser]:
        """Searches for users by keyword.

        Args:
            keyword (str): The keyword to search for.
            lang (str, optional): The language code used for the request. Defaults to None.

        Returns:
            List[PartialUser]: A list of partial user objects that match the search criteria.
        """
        data = await self.request_bbs(
            "community/search/wapi/search/user",
            lang=lang,
            params={"keyword": keyword, "page_size": 20},
        )
        return [PartialUser(**i["user"]) for i in data["list"]]

    async def get_user_info(
        self,
        accident: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> FullUser:
        """Gets user information for the current or specified user.

        Args:
            accident (int, optional): The user ID to get information for. Defaults to None.
            lang (str, optional): The language code used for the request. Defaults to None.

        Returns:
            FullUser: A full user object for the specified user.
        """
        if self.region == Region.OVERSEAS:
            url = "/community/painter/wapi/user/full"
        elif self.region == Region.CHINESE:
            url = "/user/wapi/getUserFullInfo"
        else:
            raise TypeError(f"{self.region!r} is not a valid region.")

        data = await self.request_bbs(
            endpoint=url,
            lang=lang,
            params={"uid": accident} if accident else None,
        )
        return FullUser(**data["user_info"])

    async def get_recommended_users(self, *, limit: int = 200) -> list[PartialUser]:
        """Gets a list of recommended active users.

        Args:
            limit (int, optional): The maximum number of users to retrieve. Defaults to 200.

        Returns:
            list of PartialUser: A list of partial user objects for recommended active users.
        """
        data = await self.request_bbs(
            "community/user/wapi/recommendActive",
            params={"page_size": limit},
        )
        return [PartialUser(**i["user"]) for i in data["list"]]

    async def get_genshin_announcements(
        self,
        player_id: Optional[str] = None,
        *,
        lang: Optional[str] = None,
    ) -> list[Announcement]:
        """Gets a list of Genshin Impact game announcements.

        Args:
            player_id (str, optional): The player ID to get announcements for. Defaults to None.
            lang (str, optional): The language code used for the request. Defaults to None.

        Returns:
            List[Announcement]: A list of announcement objects for the specified player.
        """
        player_id = self.player_id or player_id
        if player_id is None:
            player_id = 900000005

        params = {
            "game": "hk4e",
            "game_biz": "hk4e_global",
            "bundle_id": "hk4e_global",
            "platform": "pc",
            "region": recognize_genshin_server(player_id),
            "uid": player_id,
            "level": 8,
            "lang": lang or self.lang,
        }

        info, details = await asyncio.gather(
            self.request_bbs(
                HK4E_URL / "announcement/api/getAnnList",
                lang=lang,
                params=params,
            ),
            self.request_bbs(
                HK4E_URL / "announcement/api/getAnnContent",
                lang=lang,
                params=params,
            ),
        )

        announcements: list[dict[str, Any]] = []
        for sublist in info["list"]:
            for info in sublist["list"]:
                detail = next((i for i in details["list"] if i["ann_id"] == info["ann_id"]), None)
                announcements.append({**info, **(detail or {})})

        return [Announcement(**i) for i in announcements]

    async def redeem_code(
        self,
        code: str,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> dict:
        """Redeems a gift code for the current or specified user.

        Args:
            code (str): The gift code to redeem.
            player_id (int, optional): The player ID to redeem the code for. Defaults to None.
            lang (str, optional): The language code used for the request. Defaults to None.
        """
        player_id = self.player_id or player_id
        url = CODE_URL.get_url(self.region, self.game)
        params = {
            "uid": player_id,
            "region": recognize_server(player_id, self.game),
            "cdkey": code,
            "game_biz": recognize_game_biz(player_id, self.game),
            "lang": create_short_lang_code(lang or self.lang),
        }

        if self.game is Game.STARRAIL:
            return await self.request_bbs(
                url,
                data=params,
            )
        return await self.request_bbs(
            url,
            params=params,
        )

    async def redeem_code_by_hoyolab(
        self,
        code: str,
        player_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> dict:
        """Redeems a gift code for the current or specified user.

        Args:
            code (str): The gift code to redeem.
            player_id (int, optional): The player ID to redeem the code for. Defaults to None.
            lang (str, optional): The language code used for the request. Defaults to None.
        """
        player_id = self.player_id or player_id
        url = CODE_HOYOLAB_URL.get_url(self.region, self.game)
        params = {
            "uid": player_id,
            "region": recognize_server(player_id, self.game),
            "cdkey": code,
            "game_biz": recognize_game_biz(player_id, self.game),
            "lang": create_short_lang_code(lang or self.lang),
        }
        return await self.request_bbs(url, params=params)

    async def get_game_accounts(self, *, lang: Optional[str] = None) -> list[Account]:
        """Get the game accounts of the currently logged-in user.

        Returns:
            List[Account]: A list of account info objects.
        """
        data = await self.request_bbs(
            TAKUMI_URL.get_url(self.region) / "binding/api/getUserGameRolesByCookie",
            lang=lang,
        )
        return [Account(**i) for i in data["list"]]

    async def get_genshin_accounts(self, *, lang: Optional[str] = None) -> list[Account]:
        """Get the genshin accounts of the currently logged-in user.

        Returns:
            List[Account]: A list of account info objects of genshin accounts.
        """
        accounts = await self.get_game_accounts(lang=lang)
        return [account for account in accounts if account.game == Game.GENSHIN]

    async def get_starrail_accounts(self, *, lang: Optional[str] = None) -> list[Account]:
        """Get the starrail accounts of the currently logged-in user.

        Returns:
            List[Account]: A list of account info objects of starrail accounts.
        """
        accounts = await self.get_game_accounts(lang=lang)
        return [account for account in accounts if account.game == Game.STARRAIL]

    async def get_zzz_accounts(self, *, lang: Optional[str] = None) -> list[Account]:
        """Get the zzz accounts of the currently logged-in user.

        Returns:
            List[Account]: A list of account info objects of zzz accounts.
        """
        accounts = await self.get_game_accounts(lang=lang)
        return [account for account in accounts if account.game == Game.ZZZ]

    async def request_accompany_role(self, role_id: int, topic_id: int, *, lang: Optional[str] = None) -> AccompanyRole:
        """Accompany a role to a topic.

        Args:
            role_id (int): The role ID to accompany.
            topic_id (int): The topic ID to accompany the role to.
            lang (str, optional): The language code used for the request. Defaults to None.

        Returns:
            AccompanyRole: An accompany role object.
        """
        params = {"role_id": role_id, "topic_id": topic_id}
        data = await self.request_bbs(
            "community/apihub/api/user/accompany/role",
            lang=lang,
            params=params,
        )
        return AccompanyRole(**data)

    async def get_accompany_role(self, role_id: int, *, lang: Optional[str] = None) -> AccompanyRoleInfo:
        """Get the information related to an accompany role.

        Args:
            role_id (int): The role ID to get information for.
            lang (str, optional): The language code used for the request. Defaults to None.

        Returns:
            AccompanyRoleInfo: An accompany role info object.
        """
        params = {"role_id": role_id}
        data = await self.request_bbs(
            "community/painter/api/role/user/accompany_info",
            lang=lang,
            params=params,
        )
        return AccompanyRoleInfo(**data)

    async def get_accompany_roles(self, *, lang: Optional[str] = None) -> list[AccompanyRoleBasic]:
        """Get a list of accompany roles.

        Args:
            lang (str, optional): The language code used for the request. Defaults to None.

        Returns:
            List[AccompanyRoleBasic]: A list of accompany role basic objects.
        """
        data = await self.request_bbs(
            "community/painter/api/getChannelRoleList",
            lang=lang,
            method="POST",
        )
        game = data.get("game_roles_list", [])
        roles = []
        for g in game:
            for r in g.get("role_list", []):
                basic = r.get("basic")
                if basic:  # 确保 "basic" 键存在且有有效值
                    roles.append(AccompanyRoleBasic(**basic))
        return roles
