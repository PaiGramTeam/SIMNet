from typing import TypeVar, Union, Mapping, Optional, Sequence, Dict, List, Tuple, Any

RT = TypeVar("RT", bound="BaseClient")

URLTypes = Union["URL", str]

CookieTypes = Union["Cookie", Dict[str, str], List[Tuple[str, str]]]
RequestData = Mapping[str, Any]
PrimitiveData = Optional[Union[str, int, float, bool]]
QueryParamTypes = Union[
    "QueryParams",
    Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]],
    List[Tuple[str, PrimitiveData]],
    Tuple[Tuple[str, PrimitiveData], ...],
    str,
    bytes,
]
HeaderTypes = Union[
    "Headers",
    Mapping[str, str],
    Mapping[bytes, bytes],
    Sequence[Tuple[str, str]],
    Sequence[Tuple[bytes, bytes]],
]
TimeoutTypes = Union[
    Optional[float],
    Tuple[Optional[float], Optional[float], Optional[float], Optional[float]],
    "Timeout",
]
