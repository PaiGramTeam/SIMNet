from typing import Any, Optional, Dict, Union, Tuple, Type, NoReturn


class ApiHelperException(Exception):
    """Base class for ApiHelper errors."""


class NetworkError(ApiHelperException):
    """Base class for exceptions due to networking errors."""


class TimedOut(NetworkError):
    """Raised when a request took too long to finish."""


class BadRequest(ApiHelperException):
    """Raised when an API request cannot be processed correctly.

    Attributes:
        status_code (int): The status code of the response.
        ret_code (int): The error code of the response.
        original (str): The original error message of the response.
        message (str): The formatted error message of the response.
    """

    def __init__(
        self,
        response: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        self.status_code = status_code or 0
        self.ret_code = response.get("retcode", 0) if response else 0
        self.original = response.get("message", "") if response else ""
        self.message = message or self.original

        display_code = self.ret_code or self.status_code
        display_message = (
            f"[{display_code}] {self.message}" if display_code else self.message
        )

        super().__init__(display_message)

    def __repr__(self) -> str:
        response = {
            "status_code": self.status_code,
            "retcode": self.ret_code,
            "message": self.original,
        }
        return f"{type(self).__name__}({repr(response)})"

    @property
    def response(self) -> dict[str, Union[str, Any, None]]:
        return {"retcode": self.ret_code, "message": self.original}


class InternalDatabaseError(BadRequest):
    """Internal database error."""

    ret_code = -1


class AccountNotFound(BadRequest):
    """Tried to get data with an invalid uid."""

    message = "Could not find user; uid may be invalid."


class DataNotPublic(BadRequest):
    """User hasn't set their data to public."""

    message = "User's data is not public."


class CookieException(BadRequest):
    """Base error for cookies."""


class InvalidCookies(CookieException):
    """Cookies weren't valid."""

    ret_code = -100
    message = "Cookies are not valid."


class TooManyRequests(CookieException):
    """Made too many requests and got ratelimited."""

    ret_code = 10101
    message = "Cannot get data for more than 30 accounts per cookie per day."


class VisitsTooFrequently(BadRequest):
    """Visited a page too frequently.

    Must be handled with exponential backoff.
    """

    ret_code = -110
    message = "Visits too frequently."


class AlreadyClaimed(BadRequest):
    """Already claimed the daily reward today."""

    ret_code = -5003
    message = "Already claimed the daily reward today."


class AuthkeyException(BadRequest):
    """Base error for authkeys."""


class InvalidAuthkey(AuthkeyException):
    """Authkey is not valid."""

    ret_code = -100
    message = "Authkey is not valid."


class AuthkeyTimeout(AuthkeyException):
    """Authkey has timed out."""

    ret_code = -101
    message = "Authkey has timed out."


class RedemptionException(BadRequest):
    """Exception caused by redeeming a code."""


class RedemptionInvalid(RedemptionException):
    """Invalid redemption code."""

    message = "Invalid redemption code."


class RedemptionCooldown(RedemptionException):
    """Redemption is on cooldown."""

    message = "Redemption is on cooldown."


class RedemptionClaimed(RedemptionException):
    """Redemption code has been claimed already."""

    message = "Redemption code has been claimed already."


_TBR = Type[BadRequest]
_errors: Dict[int, Union[_TBR, str, Tuple[_TBR, Optional[str]]]] = {
    # misc hoyolab
    -100: InvalidCookies,
    -108: "Invalid language.",
    -110: VisitsTooFrequently,
    # game record
    10001: InvalidCookies,
    -10001: "Malformed request.",
    -10002: "No genshin account associated with cookies.",
    # database game record
    10101: TooManyRequests,
    10102: DataNotPublic,
    10103: (
        InvalidCookies,
        "Cookies are valid but do not have a hoyolab account bound to them.",
    ),
    10104: "Cannot view real-time notes of other users.",
    # calculator
    -500001: "Invalid fields in calculation.",
    -500004: VisitsTooFrequently,
    -502001: "User does not have this character.",
    -502002: "Calculator sync is not enabled.",
    # mixin
    -1: InternalDatabaseError,
    1009: AccountNotFound,
    # redemption
    -1065: RedemptionInvalid,
    -1071: InvalidCookies,
    -1073: (AccountNotFound, "Account has no game account bound to it."),
    -2001: (RedemptionInvalid, "Redemption code has expired."),
    -2003: (RedemptionInvalid, "Redemption code is incorrectly formatted."),
    -2004: RedemptionInvalid,
    -2014: (RedemptionInvalid, "Redemption code not activated"),
    -2016: RedemptionCooldown,
    -2017: RedemptionClaimed,
    -2018: RedemptionClaimed,
    -2021: (
        RedemptionException,
        "Cannot claim codes for accounts with adventure rank lower than 10.",
    ),
    # rewards
    -5003: AlreadyClaimed,
    # chinese
    1008: AccountNotFound,
    -1104: "This action must be done in the app.",
}


ERRORS: Dict[int, Tuple[_TBR, Optional[str]]] = {
    ret_code: (
        (exc, None)
        if isinstance(exc, type)
        else (BadRequest, exc)
        if isinstance(exc, str)
        else exc
    )
    for ret_code, exc in _errors.items()
}


def raise_for_ret_code(data: Dict[str, Any]) -> NoReturn:
    """Raise an equivalent error to a response.

    Args:
        data (dict): The response data.

    Raises:
        InvalidAuthkey: If the authkey is invalid.
        AuthkeyTimeout: If the authkey has timed out.
        AuthkeyException: If there is an authkey exception.
        RedemptionException: If there is a redemption exception.
        BadRequest: If there is a bad request.

    game record:
        10001 = invalid cookie
        101xx = generic errors
    authkey:
        -100 = invalid authkey
        -101 = authkey timed out
    code redemption:
        20xx = invalid code or state
        -107x = invalid cookies
    daily reward:
        -500x = already claimed the daily reward
    """
    r, m = data.get("retcode", 0), data.get("message", "")

    if m.startswith("authkey"):
        if r == -100:
            raise InvalidAuthkey(data)
        if r == -101:
            raise AuthkeyTimeout(data)
        raise AuthkeyException(data)

    if r in ERRORS:
        exc_type, msg = ERRORS[r]
        raise exc_type(data, msg)

    if "redemption" in m:
        raise RedemptionException(data)

    raise BadRequest(data)
