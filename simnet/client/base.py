import logging
import uuid
from types import TracebackType
from typing import AsyncContextManager, Type, Optional, Any

from httpx import AsyncClient, TimeoutException, Response, HTTPError, Timeout

from simnet.client.cookies import Cookies
from simnet.client.headers import Headers
from simnet.errors import TimedOut, NetworkError, BadRequest, raise_for_ret_code
from simnet.utils.ds import generate_dynamic_secret
from simnet.utils.enum_ import Region
from simnet.utils.types import (
    RT,
    HeaderTypes,
    CookieTypes,
    RequestData,
    QueryParamTypes,
    TimeoutTypes,
)

_LOGGER = logging.getLogger("SIMNet.BaseClient")

__all__ = ("BaseClient",)


class BaseClient(AsyncContextManager["BaseClient"]):
    """
    This is the base class for simnet clients. It provides common methods and properties for simnet clients.

    Args:
        cookies (Optional[CookieTypes], optional): The cookies used for the client.
        headers (Optional[HeaderTypes], optional): The headers used for the client.
        account_id (Optional[int], optional): The account id used for the client.
        player_id (Optional[int], optional): The player id used for the client.
        region (Region, optional): The region used for the client.
        lang (str, optional): The language used for the client.
        timeout (Optional[TimeoutTypes], optional): Timeout configuration for the client.

    Attributes:
        cookies (CookieTypes): The cookies used for the client.
        headers (HeaderTypes): The headers used for the client.
        account_id (Optional[int]): The account id used for the client.
        player_id (Optional[int]): The player id used for the client.
        region (Region): The region used for the client.
        lang (str): The language used for the client.
    """

    _device_id = str(uuid.uuid3(uuid.NAMESPACE_URL, "SIMNet"))

    def __init__(
        self,
        cookies: Optional[CookieTypes] = None,
        headers: Optional[HeaderTypes] = None,
        account_id: Optional[int] = None,
        player_id: Optional[int] = None,
        region: Region = Region.OVERSEAS,
        lang: str = "en-us",
        timeout: Optional[TimeoutTypes] = None,
    ) -> None:
        """Initialize the client with the given parameters."""
        if timeout is None:
            timeout = Timeout(
                connect=5.0,
                read=5.0,
                write=5.0,
                pool=1.0,
            )

        self.cookies = Cookies(cookies)
        self.headers = Headers(headers)
        self.player_id = player_id
        self.account_id = account_id
        self.client = AsyncClient(cookies=self.cookies, timeout=timeout)
        self.region = region
        self.lang = lang

    def get_player_id(self) -> Optional[int]:
        """Get the player id used for the client."""
        player_id = self.player_id or self.cookies.account_id
        return player_id

    @property
    def device_name(self) -> str:
        """Get the device name used for the client."""
        return "SIMNet Build 114514"

    @property
    def device_id(self) -> str:
        """Get the device id used for the client."""
        if self.account_id is not None:
            return str(uuid.uuid3(uuid.NAMESPACE_URL, str(self.account_id)))
        return self._device_id

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
            return self
        except Exception as exc:
            await self.shutdown()
            raise exc

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
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

    def get_default_header(self, header: HeaderTypes):
        """Get the default header for API requests.

        Args:
            header (HeaderTypes): The header to use.

        Returns:
            Headers: The default header with added fields.
        """
        header = Headers(header)
        header["user-agent"] = self.user_agent
        header["x-rpc-app_version"] = self.app_version
        header["x-rpc-client_type"] = self.client_type
        header["x-rpc-device_id"] = self.device_id
        return header

    def get_lab_api_header(
        self,
        header: HeaderTypes,
        lang: Optional[str] = None,
        ds: str = None,
        ds_type: str = None,
        new_ds: bool = False,
        data: Any = None,
        params: Optional[QueryParamTypes] = None,
    ):
        """Get the lab API header for API requests.

        Args:
            header (HeaderTypes): The header to use.
            lang (Optional[str], optional): The language to use for overseas regions. Defaults to None.
            ds (str, optional): The DS string to use. Defaults to None.
            ds_type (str, optional): The DS type to use. Defaults to None.
            new_ds (bool, optional): Whether to generate a new DS. Defaults to False.
            data (Any, optional): The data to use. Defaults to None.
            params (Optional[QueryParamTypes], optional): The query parameters to use. Defaults to None.
        Returns:
            Headers: The lab API header with added fields.
        """
        header = Headers(header)
        header["user-agent"] = self.user_agent
        header["x-rpc-app_version"] = self.app_version
        header["x-rpc-client_type"] = self.client_type
        header["x-rpc-device_id"] = self.device_id
        if self.region == Region.OVERSEAS:
            header["x-rpc-language"] = self.lang or lang
        if ds is None:
            app_version, client_type, ds = generate_dynamic_secret(
                self.region, ds_type, new_ds, data, params
            )
            header["x-rpc-app_version"] = app_version
            header["x-rpc-client_type"] = client_type
        header["DS"] = ds
        return header

    async def request(
        self,
        method: str,
        url: str,
        data: Optional[RequestData] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ) -> Response:
        """Make an HTTP request and return the response.

        This method makes an HTTP request with the specified HTTP method, URL, request parameters, headers,
        and JSON payload. It catches common HTTP errors and raises a `NetworkError` or `TimedOut` exception
        if the request times out.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (str): The URL to send the request to.
            data (Optional[RequestData]): The request data to include in the body of the request.
            json (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.

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
        url: str,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ):
        """Make an API request and return the data.

        This method makes an API request using the `request()` method
        and returns the data from the response if it is successful.
        If the response contains an error, it raises a `BadRequest` exception.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (str): The URL to send the request to.
            json (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.

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
        # if "application/json" in response.headers.get("Content-Type", ""):
        if not response.is_error:
            data = response.json()
            ret_code = data.get("retcode")
            if response.is_error or ret_code != 0:
                raise_for_ret_code(data)
            return data["data"]
        raise BadRequest(status_code=response.status_code, message=response.text)

    async def request_lab(
        self,
        url: str,
        method: Optional[str] = None,
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
        lang: Optional[str] = None,
        new_ds: bool = False,
        ds_type: str = None,
    ):
        """Make a request to the lab API and return the data.

        This method makes a request to the lab API using the `request_api()` method
        and returns the data from the response if it is successful.
        It also adds headers for the lab API and handles the case where the method is not specified.

        Args:
            url (str): The URL to send the request to.
            method (Optional[str]): The HTTP method to use for the request (e.g., "GET", "POST").
            data (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.
            lang (Optional[str]): The language of the request (e.g., "en", "zh").
            new_ds (bool): Whether to use a new dataset for the request.
            ds_type (str): The type of dataset to use for the request (e.g., "news", "qa").

        Returns:
            Any: The data returned by the lab API.

        """
        if method is None:
            method = "POST" if data else "GET"
        headers = self.get_lab_api_header(
            headers, ds_type=ds_type, new_ds=new_ds, lang=lang, data=data, params=params
        )
        return await self.request_api(
            method=method, url=url, json=data, params=params, headers=headers
        )
