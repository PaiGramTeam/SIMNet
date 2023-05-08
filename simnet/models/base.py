from typing import Any

from pydantic import BaseModel

try:
    import ujson as jsonlib
except ImportError:
    import json as jsonlib


class APIModel(BaseModel):
    """A Pydantic BaseModel class used for modeling JSON data returned by an API."""

    def __init__(self, **data: Any) -> None:
        for field_name, field in self.__fields__.items():
            aliases = field.field_info.extra.get("aliases")
            if aliases and aliases in data:
                data[field_name] = data.pop(aliases)
        super().__init__(**data)

    class Config:
        """A nested class defining configuration options for the APIModel."""

        json_dumps = jsonlib.dumps
        json_loads = jsonlib.loads
