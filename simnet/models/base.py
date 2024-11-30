import datetime
import typing

from pydantic import ConfigDict, BaseModel, Field as PydanticField, AfterValidator, BeforeValidator, PlainSerializer

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


def str_time_delta_parsing(v: str) -> datetime.timedelta:
    """
    Parses a string representing seconds into a timedelta object.

    Args:
        v (str): The string representing the number of seconds.

    Returns:
        datetime.timedelta: The resulting timedelta object.
    """
    return datetime.timedelta(seconds=int(v))


def str_time_delta_plain(value: datetime.timedelta) -> float:
    """
    Converts a timedelta object to its total seconds as a float.

    Args:
        value (datetime.timedelta): The timedelta object to convert.

    Returns:
        float: The total seconds represented by the timedelta object.
    """
    return value.total_seconds()


DateTimeField = typing.Annotated[datetime.datetime, AfterValidator(add_timezone)]
TimeDeltaField = typing.Annotated[
    datetime.timedelta, BeforeValidator(str_time_delta_parsing), PlainSerializer(str_time_delta_plain)
]
