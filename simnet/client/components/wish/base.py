from typing import Optional, Any, List, Dict
from urllib.parse import unquote

from simnet.client.base import BaseClient
from simnet.client.routes import GACHA_INFO_URL
from simnet.utils.enums import Game
from simnet.utils.lang import create_short_lang_code

__all__ = ("BaseWishClient",)


class BaseWishClient(BaseClient):
    """The base class for the Wish API client."""

    async def request_gacha_info(
        self,
        endpoint: str,
        game: Game,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request towards the gacha info endpoint.

        Args:
            endpoint (str): The endpoint to request data from.
            game (Game): The game to make the request for.
            lang (Optional[str] , optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str] , optional): The authorization key for making the request.
            params (Optional[Dict[str, Any]], optional): The query parameters for the request.

        Returns:
            Dict[str, Any]
                The response data as a dictionary.
        """
        params = dict(params or {})

        if authkey is None:
            raise RuntimeError("No authkey provided")

        base_url = GACHA_INFO_URL.get_url(self.region, game)
        url = base_url / endpoint

        params["authkey_ver"] = 1
        params["authkey"] = unquote(authkey)
        params["lang"] = create_short_lang_code(lang or self.lang)

        return await self.request_api("GET", url, params=params)

    async def wish_history(
        self,
        banner_types: List[int],
        limit: Optional[int] = None,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
        end_id: int = 0,
    ) -> List[object]:
        """
        Get the wish history for a list of banner types.

        Args:
            banner_types (List[int]): The list of banner types to get the wish history for.
            limit (Optional[int] , optional): The maximum number of wishes to retrieve.
                If not provided, all available wishes will be returned.
            lang (Optional[str], optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str], optional): The authorization key for making the request.
            end_id  (int, optional): The ending ID of the last wish to retrieve.

        Returns:
            List[Any]: A list of Wish objects representing the retrieved wishes.
        """

    async def get_wish_page(
        self,
        end_id: int,
        banner_type: int,
        game: Game,
        size: int = 20,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a single page of wishes.

        Args:
            end_id (int): The ending ID of the last wish to retrieve.
            banner_type (int): The type of banner to retrieve wishes from.
            game (Game): The game to make the request for.
            size (int, optional): : The number of wishes to retrieve per page, with a default value of 20.
            lang (Optional[str], optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str], optional): The authorization key for making the request.

        Returns:
            Dict[str, Any]: The response data as a dictionary.
        """
        return await self.request_gacha_info(
            "getGachaLog",
            game=game,
            lang=lang,
            authkey=authkey,
            params=dict(gacha_type=banner_type, size=size, end_id=end_id, game_biz=game.value),
        )

    async def get_banner_names(
        self,
        game: Game,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
    ) -> Dict[int, str]:
        """
        Get a list of banner names.

        Args:
            game (Game): The game to make the request for.
            lang (Optional[str], optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str], optional): The authorization key for making the request.

        Returns:
            Dict[int, str]: A dictionary mapping banner type IDs to their corresponding names.
        """
        data = await self.request_gacha_info(
            "getConfigList",
            game=game,
            lang=lang,
            authkey=authkey,
        )
        return {int(i["key"]): i["name"] for i in data["gacha_type_list"]}
