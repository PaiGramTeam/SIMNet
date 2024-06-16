from typing import Optional, Any, Dict

from simnet.client.base import BaseClient
from simnet.client.routes import SELF_HELP_URL
from simnet.utils.enums import Game

__all__ = ("BaseSelfHelpClient",)


class BaseSelfHelpClient(BaseClient):
    """Base self-help component."""

    async def request_self_help(
        self,
        endpoint: str,
        *,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request towards the ys ledger endpoint.

        Args:
            endpoint (str): The endpoint to request data from
            game (Optional[Game], optional): The game to get the ledger for.
            lang (Optional[str], optional): The language code to use for the request.
            params (Optional[Dict[str, Any]], optional): The query parameters to use for the request.

        Returns:
            Dict[str, Any]: The response data.
        """
        game = game or self.game

        params = params or {}

        url = SELF_HELP_URL.get_url(self.region, game) / endpoint

        params["sign_type"] = "2"
        params["auth_appid"] = "csc"
        params["authkey_ver"] = "1"

        params["lang"] = lang or self.lang

        return await self.request_lab(url, params=params)
