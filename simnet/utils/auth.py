"""Auth utilities."""

import hmac
import typing
from hashlib import sha256

from ..client.headers import Headers
from .constants import APP_KEYS, GAME_BIZS

if typing.TYPE_CHECKING:
    from .enums import Game, Region

GAME_LOGIN_HEADERS = {
    "x-rpc-client_type": "1",
    "x-rpc-channel_id": "1",
}


def get_game_login_headers(device_id: str, game: "Game", region: "Region") -> Headers:
    """Get the game login headers for the given `game` and `region`."""
    headers = Headers(GAME_LOGIN_HEADERS)
    headers["x-rpc-game_biz"] = GAME_BIZS[region][game]
    headers["x-rpc-device_id"] = device_id
    return headers


def generate_sign(data: dict[str, typing.Any], game: "Game", region: "Region") -> str:
    """Generate a sign for the given `data` and `app_key`."""
    key = APP_KEYS[game][region]
    string = ""
    for k in sorted(data.keys()):
        string += k + "=" + str(data[k]) + "&"
    return hmac.new(key.encode(), string[:-1].encode(), sha256).hexdigest()
