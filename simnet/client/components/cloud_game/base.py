from typing import Any, Optional

from simnet.client.base import BaseClient
from simnet.client.routes import CLOUD_GAME_URL
from simnet.utils.auth import get_combo_token
from simnet.utils.enums import Game, Region
from simnet.utils.types import QueryParamTypes


class BaseCloudGameClient(BaseClient):
    """Base client for CloudGameClient."""

    @property
    def cloud_game_combo_token_key(self) -> str:
        return f"cg_combo_token_{self.game.value}_{self.region.value}"

    @property
    def cloud_game_combo_token(self) -> str:
        return self.cookies.get(self.cloud_game_combo_token_key, "")

    @cloud_game_combo_token.setter
    def cloud_game_combo_token(self, value: str) -> None:
        self.client.cookies.set(self.cloud_game_combo_token_key, value)

    async def request_cloud_game(
        self,
        method: str,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        lang: Optional[str] = None,
        region: Optional[Region] = None,
        game: Optional[Game] = None,
    ):
        """Make a request towards the cloud game endpoint.

        Args:
            method (str): The HTTP method to use for the request
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
        base_url = CLOUD_GAME_URL.get_url(region or self.region, game or self.game)
        url = base_url / endpoint

        combo_token = get_combo_token(
            self.account_id, self.cloud_game_combo_token, game or self.game, region or self.region
        )

        lang = lang or self.lang
        headers = {"x-rpc-combo_token": combo_token, "x-rpc-language": lang}

        return await self.request_api(method, url, data, params, headers)

    async def get_cloud_game_wallet(self):
        """Get the wallet data for the cloud game."""
        return await self.request_cloud_game("GET", "wallet/wallet/get")
