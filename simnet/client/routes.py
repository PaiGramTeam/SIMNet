from typing import Dict, Union
from urllib.parse import urljoin

from httpx import URL as _URL

from simnet.utils.enum_ import Region, Game

URLTypes = Union["URL", str]

__all__ = (
    "URL",
    "BaseRoute",
    "Route",
    "InternationalRoute",
    "GameRoute",
    "RECORD_URL",
    "GACHA_INFO_URL",
    "AUTH_URL",
    "GET_COOKIES_TOKEN_BY_STOKEN_URL",
    "GET_LTOKEN_BY_STOKEN_URL",
    "AUTH_KEY_URL",
    "HK4E_LOGIN_URL",
)


class URL(_URL):
    """A subclass of httpx's URL class, with additional convenience methods for URL manipulation."""

    def join(self, url: URLTypes) -> "URL":
        """
        Join the current URL with the given URL.

        Args:
            url (Union[URL, str]): The URL to join with.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return URL(urljoin(str(self), str(URL(url))))

    def __truediv__(self, url: URLTypes) -> "URL":
        """
        Append the given URL to the current URL using the '/' operator.

        Args:
            url (Union[URL, str]): The URL to append.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return URL(urljoin(str(self) + "/", str(URL(url))))


class BaseRoute:
    """A base class for defining routes with useful metadata."""


class Route(BaseRoute):
    """A standard route with a single URL."""

    url: URL

    def __init__(self, url: str) -> None:
        """
        Initialize a Route instance.

        Args:
            url (str): The URL for this route.

        """
        self.url = URL(url)

    def get_url(self) -> URL:
        """
        Get the URL for this route.

        Returns:
            URL: The URL for this route.

        """
        return self.url


class InternationalRoute(BaseRoute):
    """A route with URLs for both the overseas and Chinese regions."""

    urls: Dict[Region, URL]

    def __init__(self, overseas: str, chinese: str) -> None:
        """
        Initialize an InternationalRoute instance.

        Args:
            overseas (str): The URL for the overseas region.
            chinese (str): The URL for the Chinese region.

        """
        self.urls = {
            Region.OVERSEAS: URL(overseas),
            Region.CHINESE: URL(chinese),
        }

    def get_url(self, region: Region) -> URL:
        """
        Get the URL for the given region.

        Args:
            region (Region): The region to get the URL for.

        Returns:
            URL: The URL for the given region.

        Raises:
            RuntimeError: If the given region is not supported.

        """
        if not self.urls[region]:
            raise RuntimeError(f"URL does not support {region.name} region.")

        return self.urls[region]


class GameRoute(BaseRoute):
    """A route with URLs for different games and regions."""

    urls: Dict[Region, Dict[Game, URL]]

    def __init__(
        self,
        overseas: Dict[str, str],
        chinese: Dict[str, str],
    ) -> None:
        """
        Initialize a GameRoute instance.

        Args:
            overseas (Dict[str, str]): A dictionary mapping game names to URLs for the overseas region.
            chinese (Dict[str, str]): A dictionary mapping game names to URLs for the Chinese region.

        """
        self.urls = {
            Region.OVERSEAS: {Game(game): URL(url) for game, url in overseas.items()},
            Region.CHINESE: {Game(game): URL(url) for game, url in chinese.items()},
        }

    def get_url(self, region: Region, game: Game) -> URL:
        """
        Get the URL for the given region and game.

        Args:
            region (Region): The region to get the URL for.
            game (Game): The game to get the URL for.

        Returns:
            URL: The URL for the given region and game.

        Raises:
            RuntimeError: If the given region or game is not supported.

        """
        if not self.urls[region]:
            raise RuntimeError(f"URL does not support {region.name} region.")

        if not self.urls[region][game]:
            raise RuntimeError(
                f"URL does not support {game.name} game for {region.name} region."
            )

        return self.urls[region][game]


PASSPORT_HOST = "passport-api.mihoyo.com"


RECORD_URL = InternationalRoute(
    overseas="https://bbs-api-os.hoyolab.com/game_record",
    chinese="https://api-takumi-record.mihoyo.com/game_record/app",
)

GACHA_INFO_URL = GameRoute(
    overseas=dict(
        genshin="https://hk4e-api-os.hoyoverse.com/event/gacha_info/api",
        hkrpg="",
    ),
    chinese=dict(
        genshin="https://hk4e-api.mihoyo.com/event/gacha_info/api",
        hkrpg="https://api-takumi.mihoyo.com/common/gacha_record/api",
    ),
)

AUTH_URL = InternationalRoute(
    overseas="",
    chinese="https://api-takumi.mihoyo.com/auth/api",
)

GET_COOKIES_TOKEN_BY_STOKEN_URL = InternationalRoute(
    overseas="",
    chinese=f"https://{PASSPORT_HOST}/account/auth/api/getCookieAccountInfoBySToken",
)

GET_LTOKEN_BY_STOKEN_URL = InternationalRoute(
    overseas="",
    chinese=f"https://{PASSPORT_HOST}/account/auth/api/getLTokenBySToken",
)

AUTH_KEY_URL = InternationalRoute(
    overseas="", chinese="https://api-takumi.mihoyo.com/binding/api/genAuthKey"
)

HK4E_LOGIN_URL = InternationalRoute(
    overseas="https://sg-public-api.hoyoverse.com/common/badge/v1/login/account",
    chinese="https://api-takumi.mihoyo.com/common/badge/v1/login/account",
)
