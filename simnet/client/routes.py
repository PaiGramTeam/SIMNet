from typing import Dict, Union
from urllib.parse import urljoin

from httpx import URL as _URL

from simnet.errors import RegionNotSupported, NotSupported
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
    "REWARD_URL",
    "TAKUMI_URL",
    "CALCULATOR_URL",
    "DETAIL_LEDGER_URL",
    "INFO_LEDGER_URL",
    "HK4E_URL",
    "CODE_URL",
    "YSULOG_URL",
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

    def __bool__(self):
        """Return True if the URL is not empty.

        Returns:
            bool: True if the URL is not empty.

        """
        return str(self) != ""


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
            RegionNotSupported: If the given region is not supported.

        """
        if not self.urls[region]:
            raise RegionNotSupported(f"URL does not support {region.name} region.")

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
            RegionNotSupported: If the given region is not supported.
            GameNotSupported: If the given game is not supported.

        """
        if not self.urls[region]:
            raise RegionNotSupported(f"URL does not support {region.name} region.")

        if not self.urls[region][game]:
            raise NotSupported(f"URL does not support {game.name} game for {region.name} region.")

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

AUTH_KEY_URL = InternationalRoute(overseas="", chinese="https://api-takumi.mihoyo.com/binding/api/genAuthKey")

HK4E_LOGIN_URL = InternationalRoute(
    overseas="https://sg-public-api.hoyoverse.com/common/badge/v1/login/account",
    chinese="https://api-takumi.mihoyo.com/common/badge/v1/login/account",
)

REWARD_URL = GameRoute(
    overseas=dict(
        genshin="https://sg-hk4e-api.hoyolab.com/event/sol?act_id=e202102251931481",
        honkai3rd="https://sg-public-api.hoyolab.com/event/mani?act_id=e202110291205111",
        hkrpg="https://sg-public-api.hoyolab.com/event/luna/os/?act_id=e202303301540311",
    ),
    chinese=dict(
        genshin="https://api-takumi.mihoyo.com/event/bbs_sign_reward/?act_id=e202009291139501",
        honkai3rd="https://api-takumi.mihoyo.com/event/luna/?act_id=e202207181446311",
        hkrpg="https://api-takumi.mihoyo.com/event/luna/?act_id=e202304121516551",
    ),
)
TAKUMI_URL = InternationalRoute(
    overseas="https://api-os-takumi.mihoyo.com/",
    chinese="https://api-takumi.mihoyo.com/",
)

CALCULATOR_URL = InternationalRoute(
    overseas="https://sg-public-api.hoyoverse.com/event/calculateos/",
    chinese="https://api-takumi.mihoyo.com/event/e20200928calculate/v1/",
)

DETAIL_LEDGER_URL = GameRoute(
    overseas=dict(
        genshin="https://sg-hk4e-api.hoyolab.com/event/ysledgeros/month_detail",
        hkrpg="https://sg-public-api.hoyolab.com/event/srledger/month_detail",
    ),
    chinese=dict(
        genshin="https://hk4e-api.mihoyo.com/event/ys_ledger/monthDetail",
        hkrpg="https://api-takumi.mihoyo.com/event/srledger/month_detail",
    ),
)

INFO_LEDGER_URL = GameRoute(
    overseas=dict(
        genshin="https://sg-hk4e-api.hoyolab.com/event/ysledgeros/month_info",
        hkrpg="https://sg-public-api.hoyolab.com/event/srledger/month_info",
    ),
    chinese=dict(
        genshin="https://hk4e-api.mihoyo.com/event/ys_ledger/monthInfo",
        hkrpg="https://api-takumi.mihoyo.com/event/srledger/month_info",
    ),
)

YSULOG_URL = InternationalRoute(
    overseas="https://hk4e-api-os.hoyoverse.com/ysulog/api/",
    chinese="https://hk4e-api.mihoyo.com/ysulog/api/",
)

HK4E_URL = Route("https://sg-hk4e-api.hoyoverse.com/common/hk4e_global/")

CODE_URL = Route("https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey")
