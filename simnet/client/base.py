import logging
import typing
import uuid
from contextlib import AbstractAsyncContextManager
from types import TracebackType

from httpx import AsyncClient, HTTPError, Response, Timeout, TimeoutException

from simnet.client.cookies import Cookies
from simnet.client.headers import Headers
from simnet.errors import (
    BadRequest,
    NetworkError,
    NotSupported,
    RegionNotSupported,
    TimedOut,
    raise_for_ret_code,
)
from simnet.utils.ds import DSType, generate_dynamic_secret, hex_digest
from simnet.utils.enums import Game, Region
from simnet.utils.types import (
    RT,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestData,
    TimeoutTypes,
    URLTypes,
)

_LOGGER = logging.getLogger("SIMNet.BaseClient")

__all__ = ("BaseClient",)


class BaseClient(AbstractAsyncContextManager["BaseClient"]):
    """
    This is the base class for simnet clients. It provides common methods and properties for simnet clients.

    Args:
        cookies (typing.Optional[str, CookieTypes], typing.Optional): The cookies used for the client.
        headers (typing.Optional[HeaderTypes], typing.Optional): The headers used for the client.
        account_id (typing.Optional[int], typing.Optional): The account id used for the client.
        player_id (typing.Optional[int], typing.Optional): The player id used for the client.
        region (Region, typing.Optional): The region used for the client.
        lang (str, typing.Optional): The language used for the client.
        timeout (typing.Optional[TimeoutTypes], typing.Optional): Timeout configuration for the client.

    Attributes:
        headers (HeaderTypes): The headers used for the client.
        account_id (typing.Optional[int]): The account id used for the client.
        player_id (typing.Optional[int]): The player id used for the client.
        region (Region): The region used for the client.
        lang (str): The language used for the client.
        game (typing.Optional[Game]): The game used for the client.

    """

    game: typing.Optional[Game] = None
    __device_id = str(uuid.uuid3(uuid.NAMESPACE_URL, "SIMNet"))

    def __init__(
        self,
        cookies: typing.Optional[typing.Union[str, CookieTypes]] = None,
        headers: typing.Optional[HeaderTypes] = None,
        account_id: typing.Optional[int] = None,
        player_id: typing.Optional[int] = None,
        region: Region = Region.OVERSEAS,
        lang: str = "en-us",
        timeout: typing.Optional[TimeoutTypes] = None,
        device_id: typing.Optional[str] = None,
        device_fp: typing.Optional[str] = None,
    ) -> None:
        """Initialize the client with the given parameters."""
        if timeout is None:
            timeout = Timeout(
                connect=5.0,
                read=5.0,
                write=5.0,
                pool=1.0,
            )
        cookies = Cookies(cookies)
        self.headers = Headers(headers)
        self.player_id = player_id
        self.account_id = account_id or cookies.account_id
        self.client = AsyncClient(cookies=cookies, timeout=timeout)
        self.region = region
        self.lang = lang
        self.device_id = device_id or cookies.get("x-rpc-device_id", None)
        self.device_fp = device_fp or cookies.get("x-rpc-device_fp", None)

    @property
    def cookies(self) -> Cookies:
        """Get the cookies used for the client."""
        return Cookies(self.client.cookies.jar)

    @cookies.setter
    def cookies(self, cookies: CookieTypes) -> None:
        self.client.cookies = cookies

    @property
    def device_name(self) -> str:
        """Get the device name used for the client."""
        return "SIMNet Build 114514"

    def get_device_id(self) -> str:
        """Get the device id used for the client."""
        if self.device_id:
            return self.device_id
        if self.account_id is not None:
            return str(uuid.uuid3(uuid.NAMESPACE_URL, str(self.account_id)))
        return self.__device_id

    def get_device_fp(self) -> str:
        """Get the device fingerprint used for the client."""
        if self.device_fp:
            return self.device_fp
        return hex_digest(self.get_device_id())[:13]

    @property
    def app_version(self) -> str:
        """Get the app version used for the client."""
        if self.region == Region.CHINESE:
            return "2.46.1"
        if self.region == Region.OVERSEAS:
            return "1.5.0"
        return "null"

    @property
    def client_type(self) -> str:
        """Get the client type used for the client."""
        if self.region == Region.CHINESE:
            return "5"
        if self.region == Region.OVERSEAS:
            return "5"
        return "null"

    @property
    def user_agent(self) -> str:
        """Get the user agent used for the client."""
        if self.region == Region.CHINESE:
            return (
                f"Mozilla/5.0 (Linux; {self.device_name}) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 "
                f"miHoYoBBS/{self.app_version}"
            )
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Safari/537.36"
        )

    async def __aenter__(self: RT) -> RT:
        """Enter the async context manager and initialize the client."""
        try:
            await self.initialize()
        except Exception:
            await self.shutdown()
            raise
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        """Exit the async context manager and shutdown the client."""
        await self.shutdown()

    async def shutdown(self):
        """Shutdown the client."""
        if self.client.is_closed:
            _LOGGER.info("This Client is already shut down. Returning.")
            return

        await self.client.aclose()

    async def initialize(self):
        """Initialize the client."""

    def get_default_header(self, headers: HeaderTypes):
        """Get the default header for API requests.

        Args:
            headers (HeaderTypes): The header to use.

        Returns:
            Headers: The default header with added fields.
        """
        headers = Headers(headers)
        headers["user-agent"] = self.user_agent
        headers["x-rpc-app_version"] = self.app_version
        headers["x-rpc-client_type"] = self.client_type
        headers["x-rpc-device_id"] = self.get_device_id()
        headers["x-rpc-device_fp"] = self.get_device_fp()
        return headers

    def get_lab_api_header(
        self,
        headers: HeaderTypes,
        lang: typing.Optional[str] = None,
        ds: str = None,
        ds_type: str = None,
        new_ds: bool = False,
        data: typing.Any = None,
        params: typing.Optional[QueryParamTypes] = None,
    ):
        """Get the lab API header for API requests.

        Args:
            headers (HeaderTypes): The header to use.
            lang (typing.Optional[str], typing.Optional): The language to use for overseas regions. Defaults to None.
            ds (str, typing.Optional): The DS string to use. Defaults to None.
            ds_type (typing.Optional[DSType], typing.Optional): The DS type to use. Defaults to None.
            new_ds (bool, typing.Optional): Whether to generate a new DS. Defaults to False.
            data (Any, typing.Optional): The data to use. Defaults to None.
            params (typing.Optional[QueryParamTypes], typing.Optional): The query parameters to use. Defaults to None.
        Returns:
            Headers: The lab API header with added fields.
        """
        headers = Headers(headers)
        headers["user-agent"] = self.user_agent
        headers["x-rpc-app_version"] = self.app_version
        headers["x-rpc-client_type"] = self.client_type
        headers["x-rpc-device_id"] = self.get_device_id()
        headers["x-rpc-device_fp"] = self.get_device_fp()
        if self.region == Region.OVERSEAS:
            if self.game == Game.ZZZ:
                headers["x-rpc-lang"] = self.lang or lang
            headers["x-rpc-language"] = self.lang or lang
        if ds is None:
            app_version, client_type, ds = generate_dynamic_secret(self.region, ds_type, new_ds, data, params)
            headers["x-rpc-app_version"] = app_version
            headers["x-rpc-client_type"] = client_type
        headers["DS"] = ds
        return headers

    async def request(
        self,
        method: str,
        url: URLTypes,
        data: typing.Optional[RequestData] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
    ) -> Response:
        """Make an HTTP request and return the response.

        This method makes an HTTP request with the specified HTTP method, URL, request parameters, headers,
        and JSON payload. It catches common HTTP errors and raises a `NetworkError` or `TimedOut` exception
        if the request times out.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            data (typing.Optional[RequestData]): The request data to include in the body of the request.
            json (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Response: A `Response` object representing the HTTP response.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.

        """
        try:
            return await self.client.request(
                method,
                url,
                data=data,
                json=json,
                params=params,
                headers=headers,
            )
        except TimeoutException as exc:
            raise TimedOut from exc
        except HTTPError as exc:
            raise NetworkError from exc

    async def request_api(
        self,
        method: str,
        url: URLTypes,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
    ):
        """Make an API request and return the data.

        This method makes an API request using the `request()` method
        and returns the data from the response if it is successful.
        If the response contains an error, it raises a `BadRequest` exception.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            json (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Any: The data returned by the API.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.
            BadRequest: If the response contains an error.
        """
        response = await self.request(
            method,
            url,
            json=json,
            params=params,
            headers=headers,
        )
        if not response.is_error:
            data = response.json()
            ret_code = data.get("retcode", 0)
            if ret_code != 0:
                raise_for_ret_code(data)
            return data["data"]
        if response.status_code == 404:
            raise NotSupported("API not supported or has been removed.")
        raise BadRequest(status_code=response.status_code, message=response.text)

    async def request_lab(
        self,
        url: URLTypes,
        method: typing.Optional[str] = None,
        data: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        lang: typing.Optional[str] = None,
        new_ds: bool = False,
        ds_type: typing.Optional[DSType] = None,
    ):
        """Make a request to the lab API and return the data.

        This method makes a request to the lab API using the `request_api()` method
        and returns the data from the response if it is successful.
        It also adds headers for the lab API and handles the case where the method is not specified.

        Args:
            url (URLTypes): The URL to send the request to.
            method (typing.Optional[str]): The HTTP method to use for the request (e.g., "GET", "POST").
            data (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.
            lang (typing.Optional[str]): The language of the request (e.g., "en", "zh").
            new_ds (bool): Whether to use a new dataset for the request.
            ds_type (typing.Optional[DSType]): The type of dataset to use for the request (e.g., "news", "qa").

        Returns:
            Any: The data returned by the lab API.

        """
        if method is None:
            method = "POST" if data else "GET"
        headers = self.get_lab_api_header(headers, ds_type=ds_type, new_ds=new_ds, lang=lang, data=data, params=params)
        return await self.request_api(method=method, url=url, json=data, params=params, headers=headers)

    def region_specific(self, cn: bool) -> None:
        """Prevent function to be run with unsupported regions."""
        if cn and self.region != Region.CHINESE:
            raise RegionNotSupported
        if not cn and self.region == Region.CHINESE:
            raise RegionNotSupported
