from typing import Optional, Any, Dict, List, Literal

from simnet.client.base import BaseClient
from simnet.client.routes import CALCULATOR_URL
from simnet.models.starrail.calculator import (
    StarrailCalculatorCharacter,
    StarrailCalculatorCharacterDetails,
)
from simnet.utils.enums import Region
from simnet.utils.player import recognize_starrail_server


class StarrailCalculatorClient(BaseClient):
    """A client for retrieving data from star rail's calculator component."""

    async def request_calculator(
        self,
        endpoint: str,
        *,
        method: str = "POST",
        lang: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request towards the calculator endpoint.

        Args:
            endpoint (str): The calculator endpoint to send the request to.
            method (str): The HTTP method to use for the request (default "POST").
            lang (str): The language to use for the request (default None).
            params (dict): The parameters to include in the request URL (default None).
            data (dict): The data to include in the request body (default None).

        Returns:
            dict: The data returned by the calculator endpoint.
        """
        params = dict(params or {})

        base_url = CALCULATOR_URL.get_url(self.region, self.game)
        url = base_url / endpoint

        if method == "GET":
            params["game"] = self.game.value
            params["lang"] = lang or self.lang
            data = None
        else:
            data = dict(data or {})
            data["lang"] = lang or self.lang

        headers = {}
        if self.region == Region.CHINESE:
            headers["Referer"] = "https://webstatic.mihoyo.com/"

        data = await self.request_lab(url, method=method, params=params, data=data, headers=headers)

        return data

    async def get_calculator_characters(
        self,
        tab_from: Literal["TabOwned", "TabAll"] = "TabOwned",
        page: int = 1,
        size: int = 100,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[StarrailCalculatorCharacter]:
        """Get all characters provided by the Enhancement Progression Calculator.

        Args:
            tab_from (Literal["TabOwned", "TabAll"], optional): The tab to get characters from. Defaults to "TabOwned".
            page (int, optional): The page to get characters from. Defaults to 1.
            size (int, optional): The number of characters to get per page. Defaults to 100.
            player_id (int): The player ID to use for syncing (default None).
            lang (str): The language to use for the request (default None).

        Returns:
            list: A list of CalculatorCharacter objects representing the characters retrieved from the calculator.
        """
        player_id = player_id or self.player_id
        params = {
            "tab_from": tab_from,
            "page": page,
            "size": size,
            "uid": player_id,
            "region": recognize_starrail_server(player_id),
        }
        data = await self.request_calculator("avatar/list", method="GET", params=params, lang=lang)
        return [StarrailCalculatorCharacter(**i) for i in data.get("list", [])]

    async def get_character_details(
        self,
        character: int,
        tab_from: Literal["TabOwned", "TabAll"] = "TabOwned",
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> StarrailCalculatorCharacterDetails:
        """
        Get the weapon, artifacts and talents of a character.

        Args:
            character (int): The ID of the character to retrieve details for.
            tab_from (Literal["TabOwned", "TabAll"], optional): The tab to get characters from. Defaults to "TabOwned".
            player_id (Optional[int], optional): The player ID to use for the request. Defaults to None.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            StarrailCalculatorCharacterDetails: The details of the character.
        """
        player_id = player_id or self.player_id
        params = dict(
            item_id=int(character),
            uid=player_id,
            region=recognize_starrail_server(player_id),
            tab_from=tab_from,
            change_target_level=0,
        )
        data = await self.request_calculator(
            "avatar/detail",
            method="GET",
            lang=lang,
            params=params,
        )
        return StarrailCalculatorCharacterDetails(**data)
