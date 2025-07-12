from functools import partial
from typing import Optional

from simnet.client.components.wish.base import BaseWishClient
from simnet.models.starrail.wish import StarRailWish
from simnet.utils.enums import Game
from simnet.utils.paginator import WishPaginator

__all__ = ("StarRailWishClient",)


class StarRailWishClient(BaseWishClient):
    """The StarRailWishClient class for making requests towards the Wish API."""

    async def wish_history(
        self,
        banner_types: Optional[list[int]] = None,
        limit: Optional[int] = None,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
        end_id: int = 0,
        min_id: int = 0,
    ) -> list[StarRailWish]:
        """
        Get the wish history for a list of banner types.

        Args:
            banner_types (Optional[List[int]], optional): The banner types to get the wish history for.
            limit (Optional[int] , optional): The maximum number of wishes to retrieve.
                If not provided, all available wishes will be returned.
            lang (Optional[str], optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str], optional): The authorization key for making the request.
            end_id  (int, optional): The ending ID of the last wish to retrieve.
            min_id (int, optional): The minimum ID of the first wish to retrieve

        Returns:
            List[StarRailWish]: A list of StarRailWish objects representing the retrieved wishes.
        """
        banner_types = banner_types or [1, 2, 11, 12, 21, 22]
        if isinstance(banner_types, int):
            banner_types = [banner_types]
        wishes = []
        for banner_type in banner_types:
            paginator = WishPaginator(
                end_id,
                min_id,
                partial(
                    self.get_wish_page,
                    banner_type=banner_type,
                    game=Game.STARRAIL,
                    lang=lang,
                    authkey=authkey,
                ),
            )
            items = await paginator.get(limit)
            wishes.extend([StarRailWish(**i) for i in items])
        return sorted(wishes, key=lambda wish: wish.time.timestamp())
