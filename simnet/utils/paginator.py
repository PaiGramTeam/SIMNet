import asyncio
from typing import List, Dict, Callable, Any, Awaitable


class WishPaginator:
    """
    A paginator for fetching and processing wish data.

    Attributes:
        end_id (int): The ID of the item to stop fetching at.
        fetch_data (Callable[..., Awaitable[Dict[str, Any]]]): An asynchronous function to fetch the raw data.
    """

    def __init__(
        self,
        end_id: int,
        fetch_data: Callable[..., Awaitable[Dict[str, Any]]],
    ):
        self.end_id = end_id
        self.fetch_data = fetch_data

    async def get(self, limit: int) -> List[Dict]:
        """
        Fetches and returns the items up to the specified limit.

        Args:
            limit (int): The maximum number of items to return.

        Returns:
            List[Dict]: The list of fetched items.
        """
        all_items = []
        current_end_id = 0

        while True:
            raw_data = await self.fetch_data(end_id=current_end_id)
            items = raw_data["list"]
            if not items:
                break

            current_end_id = items[-1]["id"]

            filtered_items = [item for item in items if item["id"] != self.end_id]
            if len(filtered_items) < len(items):
                all_items.extend(filtered_items)
                break

            all_items.extend(filtered_items)
            await asyncio.sleep(0.5)

        # Return up to the specified limit.
        return all_items[: min(len(all_items), limit)] if limit else all_items
