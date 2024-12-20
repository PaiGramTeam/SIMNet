import json
from typing import Optional

from simnet.client.base import BaseClient
from simnet.client.routes import GAME_LOGIN_URL
from simnet.models.auth.cookie import GameLoginResult
from simnet.utils.auth import generate_sign, get_game_login_headers
from simnet.utils.constants import APP_IDS


class GameAuthClient(BaseClient):
    """Game sub client for AuthClient."""

    async def login_game_by_game_token(self, game_token: str, uid: Optional[str] = None) -> GameLoginResult:
        """Log in to the game."""
        if self.game is None:
            raise ValueError("No default game set.")
        if self.region is None:
            raise ValueError("No default region set.")

        url = GAME_LOGIN_URL.get_url(self.region, self.game)
        uid = uid or self.account_id
        device = self.get_device_id()
        payload = {
            "channel_id": 1,
            "device": device,
            "app_id": int(APP_IDS[self.game][self.region]),
            "data": json.dumps({"uid": str(uid), "token": game_token, "guest": False, "is_new_register": False}),
        }
        payload["sign"] = generate_sign(payload, self.game, self.region)
        headers = get_game_login_headers(device, self.game, self.region)

        data = await self.request_api("POST", url, payload, headers=headers)
        return GameLoginResult(**data)
