from simnet.client.base import BaseClient
from simnet.client.routes import PASSPORT_MA_URL


class AuthTicketAuthClient(BaseClient):
    """AuthTicket sub client for AuthClient."""

    async def get_game_token_v2_by_auth_ticket(self, app_id: str, auth_ticket: str) -> str:
        """
        Get game token by auth ticket.

        Args:
            app_id (str): The auth app id to use to get the game token.
            auth_ticket (str): The auth ticket to use to get the game token.

        Returns:
            str: The game token v2.
        """
        self.region_specific(True)
        url = PASSPORT_MA_URL.get_url(self.region) / "../ma-cn-passport/app/loginByAuthTicket"
        payload = {"ticket": auth_ticket}
        headers = {"x-rpc-app_id": app_id}
        res_data = await self.request_api("POST", url=url, json=payload, headers=headers)
        return res_data.get("token", {}).get("token")
