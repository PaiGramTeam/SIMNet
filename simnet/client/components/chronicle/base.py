from typing import Optional, Any, List

from simnet.client.base import BaseClient
from simnet.client.routes import RECORD_URL
from simnet.errors import DataNotPublic
from simnet.models.lab.record import RecordCard
from simnet.utils.enums import Region, Game
from simnet.utils.types import QueryParamTypes

__all__ = ("BaseChronicleClient",)


class BaseChronicleClient(BaseClient):
    """The base class for the Chronicle API client.

    This class provides the basic functionality for making requests to the
    Chronicle API endpoints. It is meant to be subclassed by other clients
    that provide a more specific interface to the Chronicle API.

    Attributes:
        region (Region): The region associated with the API client.
    """

    async def request_game_record(
        self,
        endpoint: str,
        endpoint_type: str = "api",
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        lang: Optional[str] = None,
        region: Optional[Region] = None,
        game: Optional[Game] = None,
    ):
        """Make a request towards the game record endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            endpoint_type (str, optional): The type of endpoint to send the request to.
            data (Optional[Any], optional): The request payload.
            params (Optional[QueryParamTypes], optional): The query parameters for the request.
            lang (Optional[str], optional): The language for the response.
            region (Optional[Region], optional): The region associated with the request.
            game (Optional[Game], optional): The game associated with the request.

        Returns:
            The response from the server.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.
            BadRequest: If the response contains an error.
        """
        base_url = RECORD_URL.get_url(region or self.region)

        if game:
            base_url = base_url / game.value / endpoint_type

        url = base_url / endpoint
        new_ds = self.region == Region.CHINESE

        return await self.request_lab(url, data=data, params=params, lang=lang, new_ds=new_ds)

    async def update_settings(
        self,
        switch_id: int,
        on: bool,
        *,
        game: Optional[Game] = None,
    ) -> None:
        """Update user settings for the Battle Chronicle.

        This method allows the user to update their settings for the Battle Chronicle.
        The settings can control whether to show the user's Battle Chronicle on their
        profile, show the user's character details in the Battle Chronicle, and enable
        real-time notes (only for Genshin Impact).

        Args:
            switch_id (int): The ID of the setting to update. Valid values are 1, 2, and 3.
                The IDs correspond to the following settings:
                1. Show your Battle Chronicle on your profile.
                2. Show your Character Details in the Battle Chronicle.
                3. Enable your Real-Time Notes. (only for Genshin Impact)
            on (bool): The new value for the setting. Set to True to turn on the setting,
                and False to turn it off.
            game (Optional[Game], optional): The game associated with the setting. Only required
                if the setting ID is 3 (for enabling real-time notes). Valid values are Game.HONKAI,
                Game.GENSHIN, and Game.STARRAIL.
        """
        if game is None and switch_id == 3:
            game = Game.GENSHIN

        game_id = {Game.HONKAI: 1, Game.GENSHIN: 2, Game.STARRAIL: 6}[game]

        await self.request_game_record(
            "card/wapi/changeDataSwitch",
            data=dict(switch_id=switch_id, is_public=on, game_id=game_id),
        )

    async def get_record_cards(
        self,
        account_id: Optional[int] = None,
        *,
        lang: Optional[str] = None,
    ) -> List[RecordCard]:
        """Get a player record cards.

        Args:
            account_id: (int, optional), the user's account ID, defaults to None
            lang: (str, optional), the language version of the request, defaults to None

        Returns:
            A list of RecordCard objects.

        Raises:
            DataNotPublic: If data is empty.
        """
        account_id = account_id or self.account_id

        data = await self.request_game_record(
            "card/wapi/getGameRecordCard",
            lang=lang,
            params=dict(uid=account_id),
        )
        if not data["list"]:
            raise DataNotPublic({"retcode": 10102})

        return [RecordCard.creat(**card) for card in data["list"]]
