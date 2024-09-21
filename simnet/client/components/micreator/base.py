from typing import Optional, Any, List

from simnet.client.base import BaseClient
from simnet.client.routes import MI_CREATOR_URL
from simnet.models.lab.mi_creator import RewardHistory, RewardHistoryAwardItem
from simnet.utils.enums import Region, Game, SocialPlatform
from simnet.utils.types import QueryParamTypes

__all__ = ("BaseMiCreatorClient",)


class BaseMiCreatorClient(BaseClient):
    """The base class for the MiCreator API client.

    This class provides the basic functionality for making requests to the
    BaseClient API endpoints. It is meant to be subclassed by other clients
    that provide a more specific interface to the BaseClient API.

    Attributes:
        region (Region): The region associated with the API client.
    """

    async def request_mi_creator(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        lang: Optional[str] = None,
        platform: Optional[SocialPlatform] = None,
        game: Optional[Game] = None,
    ):
        """Make a request towards the mi creator endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            data (Optional[Any], optional): The request payload.
            params (Optional[QueryParamTypes], optional): The query parameters for the request.
            lang (Optional[str], optional): The language for the response.
            platform (Optional[SocialPlatform], optional): The platform associated with the request.
            game (Optional[Game], optional): The game associated with the request.

        Returns:
            The response from the server.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.
            BadRequest: If the response contains an error.
        """
        base_url = MI_CREATOR_URL

        if not params:
            params = {}
        game = game or self.game
        params["game"] = {Game.GENSHIN: "hk4e"}.get(game, "")
        params["platform"] = platform.value if platform else ""

        url = base_url / endpoint

        return await self.request_lab(url, data=data, params=params, lang=lang)

    async def get_mi_creator_reward_history(
        self,
        year: int,
        month: int,
        page: int = 1,
        page_size: int = 10,
        *,
        platform: Optional[SocialPlatform] = None,
        game: Optional[Game] = None,
    ) -> RewardHistory:
        """Get a player reward history.

        Args:
            year: (int), the year of the request
            month: (int), the month of the request
            page: (int, optional), the page number, defaults to 1
            page_size: (int, optional), the number of items per page, defaults to 10
            platform: (SocialPlatform, optional), the platform associated with the request, defaults to None
            game: (Game, optional), the game associated with the request, defaults to None

        Returns:
            RewardHistory: The reward history for the player
        """
        params = {
            "page": page,
            "page_size": page_size,
            "no_empty_past_year": True,
            "time": f"{year}-{month:02d}",
        }
        data = await self.request_mi_creator(
            "reward/history",
            params=params,
            platform=platform,
            game=game,
        )
        return RewardHistory(**data)

    async def get_mi_creator_reward_count(
        self,
        platform: Optional[SocialPlatform] = None,
        game: Optional[Game] = None,
    ) -> List[RewardHistoryAwardItem]:
        """Get the reward count for the player.

        Args:
            platform: (SocialPlatform, optional), the platform associated with the request, defaults to None
            game: (Game, optional), the game associated with the request, defaults to None

        Returns:
            int: The reward count for the player
        """
        data = await self.request_mi_creator(
            "reward/count/all",
            platform=platform,
            game=game,
        )
        item_data = data.get("list", [])
        return [RewardHistoryAwardItem(**item) for item in item_data]
