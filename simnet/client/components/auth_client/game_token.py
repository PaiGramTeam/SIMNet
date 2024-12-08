from simnet.client.base import BaseClient
from simnet.client.routes import PASSPORT_MA_URL
from simnet.utils.enums import Region


class GameTokenAuthClient(BaseClient):
    """Game token sub client for AuthClient."""

    @BaseClient.region_specific(Region.CHINESE)
    async def get_stoken_v2_and_mid_by_game_token(self, game_token: str) -> tuple[str, str]:
        """
        Get stoken_v2 and mid by game token

        Args:
            game_token (str): The game token to use to retrieve the stoken_v2 and mid.

        Returns:
            Tuple[str, str]: The stoken_v2 and mid.
        """
        url = PASSPORT_MA_URL.get_url(self.region) / "app/getTokenByGameToken"
        data = {
            "account_id": self.account_id,
            "game_token": game_token,
        }
        headers = {"x-rpc-app_id": "bll8iq97cem8"}
        data = await self.request_lab(url, data=data, headers=headers)
        mid = data.get("user_info", {}).get("mid", "")
        stoken_v2 = data.get("token", {}).get("token", "")
        self.cookies.set("mid", mid)
        self.cookies.set("stoken", stoken_v2)
        return stoken_v2, mid
