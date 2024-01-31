"""This module contains functions for recognizing servers associated with different player IDs."""

from typing import Optional, Mapping, Sequence

from simnet.utils.enums import Game, Region

UID_LENGTH: Mapping[Game, int] = {
    Game.GENSHIN: 9,
    Game.STARRAIL: 9,
    Game.HONKAI: 8,
}
UID_RANGE: Mapping[Game, Mapping[Region, Sequence[int]]] = {
    Game.GENSHIN: {
        Region.OVERSEAS: (6, 7, 8, 18, 9),
        Region.CHINESE: (1, 2, 5),
    },
    Game.STARRAIL: {
        Region.OVERSEAS: (6, 7, 8, 9),
        Region.CHINESE: (1, 2, 5),
    },
    Game.HONKAI: {
        Region.OVERSEAS: (1, 2),
        Region.CHINESE: (3, 4),
    },
}


def recognize_game_uid_first_digit(player_id: int, game: Game) -> int:
    """
    Recognizes the first digit of a game UID for a given game.

    Args:
        player_id (int): The player ID to recognize the first digit for.
        game (Game): The game the player ID belongs to.

    Returns:
        int: The first digit of the player ID.

    Raises:
        ValueError: If the specified uid is not right.
    """
    length = UID_LENGTH[game] - 1
    first = int(player_id / (10**length))
    if not first:
        raise ValueError(f"player id {player_id} is not right")
    return first


def recognize_genshin_server(player_id: int) -> str:
    """Recognize which server a Genshin UID is from.

    Args:
        player_id (int): The player ID to recognize the server for.

    Returns:
        str: The name of the server associated with the given player ID.

    Raises:
        ValueError: If the player ID is not associated with any server.
    """
    server = {
        1: "cn_gf01",
        2: "cn_gf01",
        5: "cn_qd01",
        6: "os_usa",
        7: "os_euro",
        8: "os_asia",
        18: "os_asia",
        9: "os_cht",
    }.get(recognize_game_uid_first_digit(player_id, Game.GENSHIN))

    if server:
        return server

    raise ValueError(f"Player id {player_id} isn't associated with any server")


def recognize_starrail_server(player_id: int) -> str:
    """Recognize which server a StarRail UID is from.

    Args:
        player_id (int): The player ID to recognize the server for.

    Returns:
        str: The name of the server associated with the given player ID.

    Raises:
        ValueError: If the player ID is not associated with any server.
    """
    server = {
        1: "prod_gf_cn",
        2: "prod_gf_cn",
        5: "prod_qd_cn",
        6: "prod_official_usa",
        7: "prod_official_eur",
        8: "prod_official_asia",
        9: "prod_official_cht",
    }.get(recognize_game_uid_first_digit(player_id, Game.STARRAIL))

    if server:
        return server

    raise ValueError(f"player id {player_id} isn't associated with any server")


def recognize_region(player_id: int, game: Game) -> Optional[Region]:
    """
    Recognizes the region of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the region for.
        game (Game): The game the player ID belongs to.

    Returns:
        Optional[Region]: The region the player ID belongs to if it can be recognized, None otherwise.
    """
    for region, digits in UID_RANGE[game].items():
        first = recognize_game_uid_first_digit(player_id, game)
        if first in digits:
            return region

    return None


def recognize_server(player_id: int, game: Game) -> str:
    """
    Recognizes the server of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the server for.
        game (Game): The game the player ID belongs to.

    Returns:
        str: The server the player ID belongs to.

    Raises:
        ValueError: If the specified game is not supported.
    """
    if game == Game.GENSHIN:
        return recognize_genshin_server(player_id)
    if game == Game.STARRAIL:
        return recognize_starrail_server(player_id)
    raise ValueError(f"{game} is not a valid game")


def recognize_genshin_game_biz(game_uid: int) -> str:
    """Recognizes the game biz of a player ID for a game biz.

    Returns:
        str: The game biz the player ID belongs to.
    """
    return "hk4e_cn" if game_uid < 600000000 else "hk4e_global"


def recognize_starrail_game_biz(game_uid: int) -> str:
    """Recognizes the game biz of a player ID for a game biz.

    Returns:
        str: The game biz the player ID belongs to.
    """
    return "hkrpg_cn" if game_uid < 600000000 else "hkrpg_global"


def recognize_game_biz(player_id: int, game: Game) -> str:
    """
    Recognizes the game biz of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the server for.
        game (Game): The game the player ID belongs to.

    Returns:
        str: The game biz the player ID belongs to.

    Raises:
        ValueError: If the specified game is not supported.
    """
    if game == Game.GENSHIN:
        return recognize_genshin_game_biz(player_id)
    if game == Game.STARRAIL:
        return recognize_starrail_game_biz(player_id)
    raise ValueError(f"{game} is not a valid game")
