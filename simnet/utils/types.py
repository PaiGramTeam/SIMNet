from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union

if TYPE_CHECKING:
    from http.cookiejar import Cookie  # noqa: F401

    from httpx import URL, QueryParams, Timeout  # noqa: F401

    from simnet.client.base import BaseClient  # noqa: F401
    from simnet.client.headers import Headers  # noqa: F401


RT = TypeVar("RT", bound="BaseClient")

URLTypes = Union["URL", str]

CookieTypes = Union["Cookie", dict[str, str], list[tuple[str, str]]]
RequestData = Mapping[str, Any]
PrimitiveData = Optional[Union[str, int, float, bool]]
QueryParamTypes = Union[
    "QueryParams",
    Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]],
    list[tuple[str, PrimitiveData]],
    tuple[tuple[str, PrimitiveData], ...],
    str,
    bytes,
]
HeaderTypes = Union[
    "Headers",
    Mapping[str, str],
    Mapping[bytes, bytes],
    Sequence[tuple[str, str]],
    Sequence[tuple[bytes, bytes]],
]
TimeoutTypes = Union[
    Optional[float],
    tuple[Optional[float], Optional[float], Optional[float], Optional[float]],
    "Timeout",
]
