from typing import Optional, Any, Dict, List

from simnet.client.base import BaseClient
from simnet.client.routes import CALCULATOR_URL
from simnet.errors import BadRequest
from simnet.models.genshin.calculator import (
    CalculatorResult,
    CalculatorCharacter,
    CalculatorWeapon,
    CalculatorArtifact,
    CalculatorFurnishing,
    CalculatorCharacterDetails,
    CalculatorTalent,
)
from simnet.utils.enums import Region
from simnet.utils.player import recognize_genshin_server


class CalculatorClient(BaseClient):
    """A client for retrieving data from Genshin's calculator component."""

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
            params["lang"] = lang or self.lang
            data = None
        else:
            data = dict(data or {})
            data["lang"] = lang or self.lang

        headers = {}
        if self.region == Region.CHINESE:
            headers["Referer"] = (
                "https://webstatic.mihoyo.com/ys/event/e20200923adopt_calculator/index.html?"
                "bbs_presentation_style=fullscreen&bbs_auth_required=true&"
                "utm_source=bbs&utm_medium=mys&utm_campaign=icon#/"
            )

        data = await self.request_lab(url, method=method, params=params, data=data, headers=headers)

        return data

    async def _execute_calculator(
        self,
        data: Dict[str, Any],
        *,
        lang: Optional[str] = None,
    ) -> CalculatorResult:
        """Calculate the results of a builder.

        Args:
            data (dict): The data used to calculate the results.
            lang (str): The language to use for the request (default None).

        Returns:
            CalculatorResult: The calculated results.
        """
        data = await self.request_calculator("compute", lang=lang, data=data)
        return CalculatorResult(**data)

    async def _enable_calculator_sync(self, enabled: bool = True) -> None:
        """Enable data syncing in calculator.

        Args:
            enabled (bool): Whether to enable syncing (default True).
        """
        await self.request_calculator("avatar/auth", method="POST", data=dict(avatar_auth=int(enabled)))

    async def _get_calculator_items(
        self,
        slug: str,
        filters: Dict[str, Any],
        query: Optional[str] = None,
        *,
        player_id: Optional[int] = None,
        is_all: bool = False,
        sync: bool = False,
        lang: Optional[str] = None,
        autoauth: bool = True,
    ) -> List[Dict[str, Any]]:
        """Get all items of a specific slug from a calculator.

        Args:
            slug (str): The slug to get the items for.
            filters (dict): The filters to apply to the items.
            query (str): The query to search for (default None).
            player_id (int): The player ID to use for syncing (default None).
            is_all (bool): Whether to include Traveler items (default False).
            sync (bool): Whether to sync data from the calculator (default False).
            lang (str): The language to use for the request (default None).
            autoauth (bool): Whether to enable syncing if it is not already enabled (default True).

        Returns:
            list: A list of dictionaries representing the items retrieved from the calculator.
        """
        endpoint = f"sync/{slug}/list" if sync else f"{slug}/list"

        if query:
            if any(filters.values()):
                raise TypeError("Cannot specify a query and filter at the same time")

            filters = dict(keywords=query, **filters)

        payload: Dict[str, Any] = dict(page=1, size=69420, is_all=is_all, **filters)

        if sync:
            player_id = player_id or self.player_id
            payload["uid"] = player_id
            payload["region"] = recognize_genshin_server(player_id)

        try:
            data = await self.request_calculator(endpoint, lang=lang, data=payload)
        except BadRequest as e:
            if e.ret_code != -502002:  # Sync not enabled
                raise
            if not autoauth:
                raise BadRequest(e.response, "Calculator sync is not enabled") from e

            await self._enable_calculator_sync()
            data = await self.request_calculator(endpoint, lang=lang, data=payload)

        return data["list"]

    async def get_calculator_characters(
        self,
        *,
        query: Optional[str] = None,
        elements: Optional[List[int]] = None,
        weapon_types: Optional[List[int]] = None,
        include_traveler: bool = False,
        sync: bool = False,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[CalculatorCharacter]:
        """Get all characters provided by the Enhancement Progression Calculator.

        Args:
            query (str): The query to search for (default None).
            elements (list): A list of element IDs to filter by (default None).
            weapon_types (list): A list of weapon type IDs to filter by (default None).
            include_traveler (bool): Whether to include Traveler characters (default False).
            sync (bool): Whether to sync data from the calculator (default False).
            player_id (int): The player ID to use for syncing (default None).
            lang (str): The language to use for the request (default None).

        Returns:
            list: A list of CalculatorCharacter objects representing the characters retrieved from the calculator.
        """
        data = await self._get_calculator_items(
            "avatar",
            lang=lang,
            is_all=include_traveler,
            sync=sync,
            player_id=player_id,
            query=query,
            filters=dict(
                element_attr_ids=elements or [],
                weapon_cat_ids=weapon_types or [],
            ),
        )
        return [CalculatorCharacter(**i) for i in data]

    async def get_calculator_weapons(
        self,
        *,
        query: Optional[str] = None,
        types: Optional[List[int]] = None,
        rarities: Optional[List[int]] = None,
        lang: Optional[str] = None,
    ) -> List[CalculatorWeapon]:
        """Get all weapons provided by the Enhancement Progression Calculator.

        Args:
            query (Optional[str], optional): A query string to filter the results. Defaults to None.
            types (Optional[List[int]], optional): A list of weapon types to include in the results. Defaults to None.
            rarities (Optional[List[int]], optional): A list of weapon rarities to include in the results.
                Defaults to None.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            List[CalculatorWeapon]: A list of weapons provided by the Enhancement Progression Calculator.
        """
        data = await self._get_calculator_items(
            "weapon",
            lang=lang,
            query=query,
            filters=dict(
                weapon_cat_ids=types or [],
                weapon_levels=rarities or [],
            ),
        )
        return [CalculatorWeapon(**i) for i in data]

    async def get_calculator_furnishings(
        self,
        *,
        types: Optional[int] = None,
        rarities: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[CalculatorFurnishing]:
        """
        Get all furnishings provided by the Enhancement Progression Calculator.

        Args:
            types (Optional[int], optional): The type of furnishings to retrieve. Defaults to None.
            rarities (Optional[int], optional): The rarity of the furnishings to retrieve. Defaults to None.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            List[CalculatorFurnishing]: A list of furnishings provided by the Enhancement Progression Calculator.
        """
        data = await self._get_calculator_items(
            "furniture",
            lang=lang,
            filters=dict(
                cat_id=types or 0,
                weapon_levels=rarities or 0,
            ),
        )
        return [CalculatorFurnishing(**i) for i in data]

    async def get_character_details(
        self,
        character: int,
        *,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> CalculatorCharacterDetails:
        """
        Get the weapon, artifacts and talents of a character.

        Args:
            character (int): The ID of the character to retrieve details for.
            player_id (Optional[int], optional): The player ID to use for the request. Defaults to None.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            CalculatorCharacterDetails: The details of the character.
        """
        player_id = player_id or self.player_id

        data = await self.request_calculator(
            "sync/avatar/detail",
            method="GET",
            lang=lang,
            params=dict(
                avatar_id=int(character),
                uid=player_id,
                region=recognize_genshin_server(player_id),
            ),
        )
        return CalculatorCharacterDetails(**data)

    async def get_character_talents(
        self,
        character: int,
        *,
        lang: Optional[str] = None,
    ) -> List[CalculatorTalent]:
        """Get the talents of a character.

        Args:
            character (int): The ID of the character to retrieve talents for.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            List[CalculatorTalent]: A list of talents for the specified character.
        """
        data = await self.request_calculator(
            "avatar/skill_list",
            method="GET",
            lang=lang,
            params=dict(avatar_id=int(character)),
        )
        return [CalculatorTalent(**i) for i in data["list"]]

    async def get_complete_artifact_set(
        self,
        artifact: int,
        *,
        lang: Optional[str] = None,
    ) -> List[CalculatorArtifact]:
        """
        Get all artifacts that share a set with a specified artifact.

        Args:
            artifact (int): The ID of the artifact to retrieve the set for.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            List[CalculatorArtifact]: A list of artifacts that share a set with the specified artifact.
        """
        data = await self.request_calculator(
            "reliquary/set",
            method="GET",
            lang=lang,
            params=dict(reliquary_id=int(artifact)),
        )
        return [CalculatorArtifact(**i) for i in data["reliquary_list"]]

    async def _get_all_artifact_ids(self, artifact_id: int) -> List[int]:
        """Get all artifact IDs in the same set as a given artifact ID.

        Args:
            artifact_id (int): The ID of the artifact to retrieve the set for.

        Returns:
            List[int]: A list of artifact IDs that share a set with the specified artifact ID.
        """
        others = await self.get_complete_artifact_set(artifact_id)
        return [artifact_id] + [other.id for other in others]

    async def get_teapot_replica_blueprint(
        self,
        share_code: int,
        *,
        region: Optional[str] = None,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[CalculatorFurnishing]:
        """Get the furnishings used by a teapot replica blueprint.

        Args:
            share_code (int): The share code of the teapot replica blueprint to retrieve furnishings for.
            region (Optional[str], optional): The region to use for the request. Defaults to None.
            player_id (Optional[int], optional): The player ID to use for the request. Defaults to None.
            lang (Optional[str], optional): The language to use for the calculator. Defaults to None.

        Returns:
            List[CalculatorFurnishing]: A list of furnishings used by the specified teapot replica blueprint.
        """
        if not region:
            player_id = player_id or self.player_id
            region = recognize_genshin_server(player_id)

        data = await self.request_calculator(
            "furniture/blueprint",
            method="GET",
            lang=lang,
            params=dict(share_code=share_code, region=region),
        )
        return [CalculatorFurnishing(**i) for i in data["list"]]
