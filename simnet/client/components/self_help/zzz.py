from functools import partial
from typing import Optional

from simnet.client.components.self_help.base import BaseSelfHelpClient
from simnet.models.zzz.self_help import ZZZSelfHelpActionLog
from simnet.utils.enums import Game
from simnet.utils.paginator import WishPaginator


class ZZZSelfHelpClient(BaseSelfHelpClient):
    """ZZZ self-help component."""

    async def get_zzz_action_log(
        self,
        authkey: str,
        limit: Optional[int] = None,
        end_id: int = 0,
        min_id: int = 0,
        *,
        lang: Optional[str] = None,
    ) -> list[ZZZSelfHelpActionLog]:
        """
        Get the action log for a starrail user.

        Args:
            authkey: The authkey for the user.
            limit: The number of logs to get.
            end_id: The end ID for the logs.
            min_id: The minimum ID for the logs.
            lang: The language to get the logs in.

        Returns:
            List[ZZZSelfHelpActionLog]: The action logs.
        """
        paginator = WishPaginator(
            end_id,
            min_id,
            partial(
                self.request_self_help,
                endpoint="LoginRecord/GetList",
                game=Game.ZZZ,
                lang=lang,
                params={
                    "authkey": authkey,
                    "size": 100,
                    "page_id": 0,
                },
            ),
        )
        items = await paginator.get(limit)
        return [ZZZSelfHelpActionLog(**i) for i in items]
