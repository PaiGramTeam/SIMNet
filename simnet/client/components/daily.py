"""Daily reward component."""
import asyncio
from typing import Optional, Dict, Any, List

from simnet.client.base import BaseClient
from simnet.utils.ds import hex_digest
from simnet.client.routes import REWARD_URL
from simnet.models.lab.daily import DailyRewardInfo, DailyReward, ClaimedDailyReward
from simnet.utils.enum_ import Game, Region

__all__ = ("DailyRewardClient",)

from simnet.utils.player import recognize_server


class DailyRewardClient(BaseClient):
    """A client for interacting with the daily reward system."""

    async def request_daily_reward(
        self,
        endpoint: str,
        *,
        method: str = "GET",
        challenge: Optional[str] = None,
        validate: Optional[str] = None,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Makes a request to the daily reward endpoint.

        Args:
            endpoint (str): The endpoint to request.
            method (str): The HTTP method to use. Defaults to "GET".
            challenge (str): A challenge string for validating the request. Defaults to None.
            validate (str): A validation string for validating the request. Defaults to None.
            game (Game): The game to request data for. Defaults to None.
            lang (str): The language to use. Defaults to None.
            params (Dict[str, Any]): Any parameters to include in the request.

        Returns:
            A dictionary containing the response data.
        """
        new_ds: bool = False
        headers: Dict[str, str] = {}
        params = dict(params or {})
        game = game or self.game
        if self.region == Region.CHINESE:
            uid = self.player_ids[game]
            params["uid"] = uid
            params["region"] = recognize_server(uid, game)
            if challenge is not None and validate is not None:
                headers["x-rpc-challenge"] = challenge
                headers["x-rpc-validate"] = validate
                headers["x-rpc-seccode"] = f"{validate}|jordan"
            headers["Referer"] = (
                "https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?"
                "bbs_auth_required=true&act_id=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon"
            )

            headers["x-rpc-device_name"] = "Chrome 20 2023"
            headers["x-rpc-channel"] = "chrome"
            headers["x-rpc-device_model"] = "Chrome 2023"
            headers["x-rpc-sys_version"] = "13"
            headers["x-rpc-platform"] = "android"
            device_id = self.device_id
            hash_value = hex_digest(device_id)
            headers["x-rpc-device_fp"] = hash_value[:13]
            new_ds = endpoint == "sign"

        base_url = REWARD_URL.get_url(self.region, self.game or game)
        url = (base_url / endpoint).copy_merge_params(base_url.params)

        return await self.request_lab(
            url, method, params=params, headers=headers, lang=lang, new_ds=new_ds
        )

    async def get_reward_info(
        self,
        *,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
    ) -> DailyRewardInfo:
        """Gets the daily reward info for the current user.

        Args:
            game (Game): The game to request data for. Defaults to None.
            lang (str): The language to use. Defaults to None.

        Returns:
            A DailyRewardInfo object containing information about the user's daily reward status.
        """
        data = await self.request_daily_reward("info", game=game, lang=lang)
        return DailyRewardInfo(data["is_sign"], data["total_sign_day"])

    async def get_monthly_rewards(
        self,
        *,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
    ) -> List[DailyReward]:
        """Gets a list of all available rewards for the current month.

        Args:
            game (Game): The game to request data for. Defaults to None.
            lang (str): The language to use. Defaults to None.

        Returns:
            A list of DailyReward objects representing the available rewards for the current month.
        """
        data = await self.request_daily_reward(
            "home",
            game=game,
            lang=lang,
        )
        return [DailyReward(**i) for i in data["awards"]]

    async def _get_claimed_rewards_page(
        self,
        page: int,
        *,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
    ) -> List[ClaimedDailyReward]:
        """Gets a single page of claimed rewards for the current user.

        Args:
            page (int): The page number to retrieve.
            game (Game): The game to request data for. Defaults to None.
            lang (str): The language to use. Defaults to None.

        Returns:
            A list of ClaimedDailyReward objects representing the claimed rewards for the current user on the specified
                page.
        """
        data = await self.request_daily_reward(
            "award", params=dict(current_page=page), game=game, lang=lang
        )
        return [ClaimedDailyReward(**i) for i in data["list"]]

    async def claimed_rewards(
        self,
        *,
        limit: Optional[int] = None,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
    ) -> List[ClaimedDailyReward]:
        """Gets all claimed rewards for the current user.

        Args:
            limit (int): The maximum number of rewards to return. Defaults to None.
            game (Game): The game to request data for. Defaults to None.
            lang (str): The language to use. Defaults to None.

        Returns:
            A list of ClaimedDailyReward objects representing the claimed rewards for the current user.
        """
        result = []
        index = 0
        page = 1

        while True:
            if page >= 10:
                break

            fetched_items = await self._get_claimed_rewards_page(
                page, game=game, lang=lang
            )
            if not fetched_items:
                break

            # Calculate how many items should be added
            items_to_add = (
                limit - index
                if limit is not None and limit - index < len(fetched_items)
                else len(fetched_items)
            )

            result.extend(fetched_items[:items_to_add])
            index += items_to_add

            if limit is not None and index >= limit:
                break

            page += 1

        return result

    async def claim_daily_reward(
        self,
        *,
        challenge: Optional[str] = None,
        validate: Optional[str] = None,
        game: Optional[Game] = None,
        lang: Optional[str] = None,
        reward: bool = True,
    ) -> Optional[DailyReward]:
        """
        Signs into lab and claims the daily reward.

        Args:
            challenge (str): A challenge string for validating the request. Defaults to None.
            validate (str): A validation string for validating the request. Defaults to None.
            game (Game): The game to claim the reward for. Defaults to None.
            lang (str): The language to use. Defaults to None.
            reward (bool): Whether to return the claimed reward. Defaults to True.

        Returns:
            If `reward` is True, a DailyReward object representing the claimed reward. Otherwise, None.
        """
        await self.request_daily_reward(
            "sign",
            method="POST",
            game=game,
            lang=lang,
            challenge=challenge,
            validate=validate,
        )

        if not reward:
            return None

        info, rewards = await asyncio.gather(
            self.get_reward_info(game=game, lang=lang),
            self.get_monthly_rewards(game=game, lang=lang),
        )
        return rewards[info.claimed_rewards - 1]
