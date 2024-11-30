import datetime
import typing

from pydantic import ConfigDict, BaseModel, Field as PydanticField, AfterValidator, BeforeValidator, WrapSerializer

if typing.TYPE_CHECKING:
    from pydantic import SerializerFunctionWrapHandler, SerializationInfo

CN_TIMEZONE = datetime.timezone(datetime.timedelta(hours=8))


class APIModel(BaseModel):
    """A Pydantic BaseModel class used for modeling JSON data returned by an API."""

    model_config = ConfigDict(coerce_numbers_to_str=True, arbitrary_types_allowed=True)


def Field(
    default: typing.Any = None,
    alias: typing.Optional[str] = None,
    **kwargs: typing.Any,
):
    """Create an aliased field."""
    return PydanticField(default, alias=alias, **kwargs)


def add_timezone(value: datetime.datetime) -> datetime.datetime:
    """
    Adds the CN_TIMEZONE to a datetime object.

    Args:
        value (datetime.datetime): The datetime object to which the timezone will be added.

    Returns:
        datetime.datetime: The datetime object with the CN_TIMEZONE applied.
    """
    return value.astimezone(CN_TIMEZONE)


def str_time_date_plain(
    value: datetime.datetime, handler: "SerializerFunctionWrapHandler", info: "SerializationInfo"
) -> typing.Union[str, datetime.datetime]:
    """
    Converts a datetime object to its ISO 8601 string representation if the mode is JSON, otherwise uses the handler.

    Args:
        value (datetime.datetime): The datetime object to convert.
        handler (SerializerFunctionWrapHandler): The handler function to use if the mode is not JSON.
        info (SerializationInfo): Information about the serialization context.

    Returns:
        typing.Union[str, datetime.datetime]: The ISO 8601 string representation if the mode is JSON, otherwise the result of the handler.
    """
    if info.mode_is_json():
        return value.isoformat()
    return handler(value)


def str_time_delta_parsing(v: str) -> datetime.timedelta:
    """
    Parses a string representing seconds into a timedelta object.

    Args:
        v (str): The string representing the number of seconds.

    Returns:
        datetime.timedelta: The resulting timedelta object.
    """
    return datetime.timedelta(seconds=int(v))


def str_time_delta_plain(
    value: datetime.timedelta, handler: "SerializerFunctionWrapHandler", info: "SerializationInfo"
) -> typing.Union[float, datetime.timedelta]:
    """
    Converts a timedelta object to its total seconds as a float if the mode is JSON, otherwise uses the handler.

    Args:
        value (datetime.timedelta): The timedelta object to convert.
        handler (SerializerFunctionWrapHandler): The handler function to use if the mode is not JSON.
        info (SerializationInfo): Information about the serialization context.

    Returns:
        typing.Union[float, datetime.timedelta]: The total seconds as a float if the mode is JSON, otherwise the result of the handler.
    """
    if info.mode_is_json():
        return value.total_seconds()
    return handler(value)


DateTimeField = typing.Annotated[
    datetime.datetime,
    AfterValidator(add_timezone),
    WrapSerializer(str_time_date_plain),
]
TimeDeltaField = typing.Annotated[
    datetime.timedelta,
    BeforeValidator(str_time_delta_parsing),
    WrapSerializer(str_time_delta_plain),
]
