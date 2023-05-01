from typing import Optional, Any
from simnet.client.base import BaseClient
from simnet.client.routes import RECORD_URL
from simnet.utils.enum_ import Region, Game
from simnet.utils.types import QueryParamTypes


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
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        lang: Optional[str] = None,
        region: Optional[Region] = None,
        game: Optional[Game] = None,
    ):
        """Make a request towards the game record endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
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
            base_url = base_url / game.value / "api"

        url = base_url / endpoint
        new_ds = self.region == Region.CHINESE

        return await self.request_lab(
            url, data=data, params=params, lang=lang, new_ds=new_ds
        )
