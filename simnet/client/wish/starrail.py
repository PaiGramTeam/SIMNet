from typing import Optional, List
from simnet.client.wish.base import BaseWishClient
from simnet.models.starrail.wish import StarRailWish
from simnet.utils.enum_ import Game


class WishClient(BaseWishClient):
    """The WishClient class for making requests towards the Wish API."""

    async def wish_history(
        self,
        banner_types: List[int],
        limit: Optional[int] = None,
        lang: Optional[str] = None,
        authkey: Optional[str] = None,
        end_id: int = 0,
    ) -> List[StarRailWish]:
        """
        Get the wish history for a list of banner types.

        Args:
            banner_types (List[int], optional): The list of banner types to get the wish history for.
            limit (Optional[int] , optional): The maximum number of wishes to retrieve.
                If not provided, all available wishes will be returned.
            lang (Optional[str], optional): The language code to use for the request.
                If not provided, the class default will be used.
            authkey (Optional[str], optional): The authorization key for making the request.
            end_id  (int, optional): The ending ID of the last wish to retrieve.

        Returns:
            List[StarRailWish]: A list of StarRailWish objects representing the retrieved wishes.
        """
        wish: List[StarRailWish] = []
        banner_names = await self.get_banner_names(
            game=Game.STARRAIL, lang=lang, authkey=authkey
        )
        for banner_type in banner_types:
            data = await self.get_wish_page(end_id, banner_type, Game.STARRAIL)
            banner_name = banner_names[banner_type]
            wish = [StarRailWish(**i, banner_name=banner_name) for i in data["list"]]
        return wish
