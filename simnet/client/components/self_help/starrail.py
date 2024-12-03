from functools import partial
from typing import Optional

from simnet.client.components.self_help.base import BaseSelfHelpClient
from simnet.models.starrail.self_help import StarRailSelfHelpActionLog
from simnet.utils.enums import Game
from simnet.utils.paginator import WishPaginator


class StarrailSelfHelpClient(BaseSelfHelpClient):
    """Starrail self-help component."""

    async def get_starrail_action_log(
        self,
        authkey: str,
        limit: Optional[int] = None,
        end_id: int = 0,
        min_id: int = 0,
        *,
        lang: Optional[str] = None,
    ) -> list[StarRailSelfHelpActionLog]:
        """
        Get the action log for a starrail user.

        Args:
            authkey: The authkey for the user.
            limit: The number of logs to get.
            end_id: The end ID for the logs.
            min_id: The minimum ID for the logs.
            lang: The language to get the logs in.

        Returns:
            List[StarRailSelfHelpActionLog]: The action logs.
        """
        paginator = WishPaginator(
            end_id,
            min_id,
            partial(
                self.request_self_help,
                endpoint="UserInfo/GetActionLog",
                game=Game.STARRAIL,
                lang=lang,
                params={
                    "authkey": authkey,
                    "size": 100,
                    "page_id": 0,
                },
            ),
        )
        items = await paginator.get(limit)
        return [StarRailSelfHelpActionLog(**i) for i in items]
