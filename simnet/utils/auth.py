"""Auth utilities."""

import hmac
import typing
from hashlib import sha256

from ..client.headers import Headers
from .constants import APP_IDS, APP_KEYS, GAME_BIZS

if typing.TYPE_CHECKING:
    from .enums import Game, Region

GAME_LOGIN_HEADERS = {
    "x-rpc-client_type": "1",
    "x-rpc-channel_id": "1",
}


def get_combo_token(account_id: int, combo_token: str, game: "Game", region: "Region") -> str:
    """Get the combo token headers for the given `combo_token`."""
    app_id = APP_IDS[game][region]
    channel_id = 1
    biz = GAME_BIZS[region][game]
    params = {
        "app_id": str(app_id),
        "channel_id": str(channel_id),
        "open_id": str(account_id),
        "combo_token": combo_token,
    }
    sign = generate_sign(params, game, region)
    data = {
        "ai": str(app_id),
        "ci": str(channel_id),
        "oi": str(account_id),
        "ct": combo_token,
        "si": sign,
        "bi": biz,
    }
    string = ""
    for k in sorted(data.keys()):
        string += k + "=" + str(data[k]) + ";"
    return string


def get_game_login_headers(device_id: str, game: "Game", region: "Region") -> Headers:
    """Get the game login headers for the given `game` and `region`."""
    headers = Headers(GAME_LOGIN_HEADERS)
    headers["x-rpc-game_biz"] = GAME_BIZS[region][game]
    headers["x-rpc-device_id"] = device_id
    return headers


def generate_sign_by_key(data: dict[str, typing.Any], key: str) -> str:
    string = ""
    for k in sorted(data.keys()):
        string += k + "=" + str(data[k]) + "&"
    return hmac.new(key.encode(), string[:-1].encode(), sha256).hexdigest()


def generate_sign(data: dict[str, typing.Any], game: "Game", region: "Region") -> str:
    """Generate a sign for the given `data` and `app_key`."""
    key = APP_KEYS[game][region]
    return generate_sign_by_key(data, key)
