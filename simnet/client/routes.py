from typing import Union
from urllib.parse import urljoin

from httpx import URL as _URL

from simnet.errors import NotSupported, RegionNotSupported
from simnet.utils.enums import Game, Region

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
    "PASSPORT_URL",
    "PASSPORT_MA_URL",
    "WEB_ACCOUNT_URL",
    "AUTH_KEY_URL",
    "HK4E_LOGIN_URL",
    "REWARD_URL",
    "TAKUMI_URL",
    "CALCULATOR_URL",
    "DETAIL_LEDGER_URL",
    "INFO_LEDGER_URL",
    "HK4E_URL",
    "CODE_URL",
    "CODE_HOYOLAB_URL",
    "YSULOG_URL",
    "QRCODE_URL",
    "GET_FP_URL",
    "BBS_URL",
    "SELF_HELP_URL",
    "GAME_LOGIN_URL",
    "CLOUD_GAME_URL",
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

    def replace(self, old: str, new: str) -> "URL":
        """
        Replace a substring in the URL.

        Args:
            old (str): The substring to replace.
            new (str): The new substring to replace with.

        Returns:
            URL: A new URL instance with the substring replaced.

        """
        return URL(str(self).replace(old, new))


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

    def __truediv__(self, other: str) -> URL:
        """
        Append the given URL to this route using the '/' operator.

        Args:
            other (Union[URL, str]): The URL to append.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return self.url / other


class InternationalRoute(BaseRoute):
    """A route with URLs for both the overseas and Chinese regions."""

    urls: dict[Region, URL]

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

    urls: dict[Region, dict[Game, URL]]

    def __init__(
        self,
        overseas: dict[str, str],
        chinese: dict[str, str],
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


RECORD_URL = GameRoute(
    overseas={
        "genshin": "https://bbs-api-os.hoyolab.com/game_record",
        "hkrpg": "https://bbs-api-os.hoyolab.com/game_record",
        "nap": "https://sg-act-nap-api.hoyolab.com/event/game_record_zzz",
    },
    chinese={
        "genshin": "https://api-takumi-record.mihoyo.com/game_record/app",
        "hkrpg": "https://api-takumi-record.mihoyo.com/game_record/app",
        "nap": "https://api-takumi-record.mihoyo.com/event/game_record_zzz",
    },
)

GACHA_INFO_URL = GameRoute(
    overseas={
        "genshin": "https://public-operation-hk4e-sg.hoyoverse.com/gacha_info/api",
        "hkrpg": "https://public-operation-hkrpg-sg.hoyoverse.com/common/gacha_record/api/",
        "nap": "https://public-operation-nap-sg.hoyoverse.com/common/gacha_record/api",
    },
    chinese={
        "genshin": "https://public-operation-hk4e.mihoyo.com/gacha_info/api",
        "hkrpg": "https://public-operation-hkrpg.mihoyo.com/common/gacha_record/api",
        "nap": "https://public-operation-nap.mihoyo.com/common/gacha_record/api",
    },
)

AUTH_URL = InternationalRoute(
    overseas="https://api-os-takumi.mihoyo.com/auth/api",
    chinese="https://api-takumi.mihoyo.com/auth/api",
)
PASSPORT_URL = InternationalRoute(
    overseas="https://api-account-os.hoyoverse.com/account/auth/api/",
    chinese="https://passport-api.mihoyo.com/account/auth/api/",
)
PASSPORT_MA_URL = InternationalRoute(
    overseas="https://api-account-os.hoyoverse.com/account/ma-passport/",
    chinese="https://passport-api.mihoyo.com/account/ma-cn-session/",
)
WEB_ACCOUNT_URL = InternationalRoute(
    overseas="https://webapi-os.account.hoyoverse.com/Api/",
    chinese="https://webapi.account.mihoyo.com/Api/",
)

AUTH_KEY_URL = InternationalRoute(
    overseas="https://sg-public-api.hoyoverse.com/binding/api/genAuthKey",
    chinese="https://api-takumi.mihoyo.com/binding/api/genAuthKey",
)

HK4E_LOGIN_URL = InternationalRoute(
    overseas="https://sg-public-api.hoyoverse.com/common/badge/v1/login/account",
    chinese="https://api-takumi.mihoyo.com/common/badge/v1/login/account",
)

REWARD_URL = GameRoute(
    overseas={
        "genshin": "https://sg-hk4e-api.hoyolab.com/event/sol/?act_id=e202102251931481",
        "honkai3rd": "https://sg-public-api.hoyolab.com/event/mani/?act_id=e202110291205111",
        "hkrpg": "https://sg-public-api.hoyolab.com/event/luna/os/?act_id=e202303301540311",
        "nap": "https://sg-act-nap-api.hoyolab.com/event/luna/zzz/os/?act_id=e202406031448091",
    },
    chinese={
        "genshin": "https://api-takumi.mihoyo.com/event/luna/?act_id=e202311201442471",
        "honkai3rd": "https://api-takumi.mihoyo.com/event/luna/?act_id=e202207181446311",
        "hkrpg": "https://api-takumi.mihoyo.com/event/luna/?act_id=e202304121516551",
        "nap": "https://act-nap-api.mihoyo.com/event/luna/zzz/?act_id=e202406242138391",
    },
)
TAKUMI_URL = InternationalRoute(
    overseas="https://api-os-takumi.mihoyo.com/",
    chinese="https://api-takumi.mihoyo.com/",
)

CALCULATOR_URL = GameRoute(
    overseas={
        "genshin": "https://sg-public-api.hoyolab.com/event/e20200928calculate/v1/",
        "hkrpg": "https://sg-public-api.hoyolab.com/event/rpgcalc/",
    },
    chinese={
        "genshin": "https://api-takumi.mihoyo.com/event/e20200928calculate/v1/",
        "hkrpg": "https://api-takumi.mihoyo.com/event/rpgcalc/",
    },
)

DETAIL_LEDGER_URL = GameRoute(
    overseas={
        "genshin": "https://sg-hk4e-api.hoyolab.com/event/ysledgeros/month_detail",
        "hkrpg": "https://sg-public-api.hoyolab.com/event/srledger/month_detail",
        "nap": "https://sg-public-api.hoyolab.com/event/nap_ledger/month_detail",
    },
    chinese={
        "genshin": "https://hk4e-api.mihoyo.com/event/ys_ledger/monthDetail",
        "hkrpg": "https://api-takumi.mihoyo.com/event/srledger/month_detail",
        "nap": "https://api-takumi.mihoyo.com/event/nap_ledger/month_detail",
    },
)

INFO_LEDGER_URL = GameRoute(
    overseas={
        "genshin": "https://sg-hk4e-api.hoyolab.com/event/ysledgeros/month_info",
        "hkrpg": "https://sg-public-api.hoyolab.com/event/srledger/month_info",
        "nap": "https://sg-public-api.hoyolab.com/event/nap_ledger/month_info",
    },
    chinese={
        "genshin": "https://hk4e-api.mihoyo.com/event/ys_ledger/monthInfo",
        "hkrpg": "https://api-takumi.mihoyo.com/event/srledger/month_info",
        "nap": "https://api-takumi.mihoyo.com/event/nap_ledger/month_info",
    },
)

YSULOG_URL = InternationalRoute(
    overseas="https://hk4e-api-os.hoyoverse.com/common/hk4e_self_help_query/User/",
    chinese="https://hk4e-api.mihoyo.com/common/hk4e_self_help_query/User/",
)

HK4E_URL = Route("https://sg-hk4e-api.hoyoverse.com/common/hk4e_global/")

CODE_URL = GameRoute(
    overseas={
        "genshin": "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey",
        "hkrpg": "https://sg-hkrpg-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkeyRisk",
        "nap": "https://public-operation-nap.hoyoverse.com/common/apicdkey/api/webExchangeCdkey",
    },
    chinese={},
)
CODE_HOYOLAB_URL = GameRoute(
    overseas={
        "genshin": "https://sg-hk4e-api.hoyolab.com/common/apicdkey/api/webExchangeCdkeyHyl",
        "hkrpg": "https://sg-hkrpg-api.hoyolab.com/common/apicdkey/api/webExchangeCdkeyHyl",
        "nap": "https://public-operation-nap.hoyoverse.com/common/apicdkey/api/webExchangeCdkey",
    },
    chinese={},
)

QRCODE_URL = Route("https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode")

GET_FP_URL = Route("https://public-data-api.mihoyo.com/device-fp/api/getFp")

BBS_URL = InternationalRoute(
    overseas="https://bbs-api-os.hoyolab.com",
    chinese="https://bbs-api.miyoushe.com",
)

SELF_HELP_URL = GameRoute(
    overseas={},
    chinese={
        "genshin": "https://hk4e-api.mihoyo.com/common/hk4e_self_help_query",
        "hkrpg": "https://api-takumi.mihoyo.com/common/hkrpg_self_help_inquiry",
        "nap": "https://public-operation-nap.mihoyo.com/common/nap_self_help_query",
    },
)

GAME_LOGIN_URL = GameRoute(
    overseas={
        "genshin": "https://hk4e-sdk-os.hoyoverse.com/hk4e_global/combo/granter/login/v2/login",
        "honkai3rd": "https://bh3-sdk-os.hoyoverse.com/bh3_os/combo/granter/login/v2/login",
        "hkrpg": "https://hkrpg-sdk-os.hoyoverse.com/hkrpg_global/combo/granter/login/v2/login",
        "nap": "https://nap-sdk-os.hoyoverse.com/nap_global/combo/granter/login/v2/login",
    },
    chinese={
        "genshin": "https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/granter/login/v2/login",
        "honkai3rd": "https://api-sdk.mihoyo.com/bh3_cn/combo/granter/login/v2/login",
        "hkrpg": "https://hkrpg-sdk.mihoyo.com/hkrpg_cn/combo/granter/login/v2/login",
        "nap": "https://nap-sdk.mihoyo.com/nap_cn/combo/granter/login/v2/login",
    },
)

CLOUD_GAME_URL = GameRoute(
    overseas={},
    chinese={
        "genshin": "https://api-cloudgame.mihoyo.com/hk4e_cg_cn/",
        "hkrpg": "https://cg-hkrpg-api.mihoyo.com/hkrpg_cn/cg/",
        "nap": "https://cg-nap-api.mihoyo.com/nap_cn/cg/",
    },
)
