from typing import Optional, List

from simnet.client.components.self_help.base import BaseSelfHelpClient
from simnet.models.starrail.self_help import StarRailSelfHelpActionLog
from simnet.utils.enums import Game


class StarrailSelfHelpClient(BaseSelfHelpClient):
    """Starrail self-help component."""

    async def get_starrail_action_log(
        self,
        authkey: str,
        size: int = 100,
        end_id: int = 0,
        page_id: int = 0,
        *,
        lang: Optional[str] = None,
    ) -> List[StarRailSelfHelpActionLog]:
        """
        Get the action log for a starrail user.

        Args:
            authkey: The authkey for the user.
            size: The number of logs to get.
            end_id: The end ID for the logs.
            page_id: The page ID for the logs.
            lang: The language to get the logs in.

        Returns:
            List[StarRailSelfHelpActionLog]: The action logs.
        """
        params = {
            "authkey": authkey,
            "size": size,
            "end_id": end_id,
            "page_id": page_id,
        }
        data = await self.request_self_help("UserInfo/GetActionLog", game=Game.STARRAIL, lang=lang, params=params)
        return [StarRailSelfHelpActionLog(**log) for log in data["list"]]
