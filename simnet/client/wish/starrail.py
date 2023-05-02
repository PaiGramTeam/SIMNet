from functools import partial
from typing import Optional, List
from simnet.client.wish.base import BaseWishClient
from simnet.models.starrail.wish import StarRailWish
from simnet.utils.enum_ import Game
from simnet.utils.paginator import WishPaginator


class WishClient(BaseWishClient):
    """The WishClient class for making requests towards the Wish API."""

    async def wish_history(
        self,
        banner_type: int,
        limit: Optional[int] = None,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
        end_id: int = 0,
    ) -> List[StarRailWish]:
        """
        Get the wish history for a list of banner types.

        Args:
            banner_type (int, optional): The banner types to get the wish history for.
            limit (Optional[int] , optional): The maximum number of wishes to retrieve.
                If not provided, all available wishes will be returned.
            lang (Optional[str], optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str], optional): The authorization key for making the request.
            end_id  (int, optional): The ending ID of the last wish to retrieve.

        Returns:
            List[StarRailWish]: A list of StarRailWish objects representing the retrieved wishes.
        """
        banner_names = await self.get_banner_names(
            game=Game.STARRAIL, lang=lang, authkey=authkey
        )
        paginator = WishPaginator(
            end_id,
            partial(
                self.get_wish_page,
                banner_type=banner_type,
                game=Game.STARRAIL,
                authkey=authkey,
            ),
        )
        items = await paginator.get(limit)
        banner_name = banner_names[banner_type]
        wish = [StarRailWish(**i, banner_name=banner_name) for i in items]
        return wish
