import datetime
import typing

from pydantic import ConfigDict, BaseModel, Field as PydanticField, AfterValidator

CN_TIMEZONE = datetime.timezone(datetime.timedelta(hours=8))


class APIModel(BaseModel):
    """A Pydantic BaseModel class used for modeling JSON data returned by an API."""

    model_config = ConfigDict(coerce_numbers_to_str=True)


def Field(
    alias: typing.Optional[str] = None,
    default: typing.Any = None,
    **kwargs: typing.Any,
):
    """Create an aliased field."""
    return PydanticField(default, alias=alias, **kwargs)


def add_timezone(value: datetime.datetime) -> datetime.datetime:
    return value.astimezone(CN_TIMEZONE)


DateTimeField = typing.Annotated[datetime.datetime, AfterValidator(add_timezone)]
