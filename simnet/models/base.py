from pydantic import BaseModel

try:
    import ujson as jsonlib
except ImportError:
    import json as jsonlib


class APIModel(BaseModel):
    """A Pydantic BaseModel class used for modeling JSON data returned by an API."""

    class Config:
        """A nested class defining configuration options for the APIModel."""

        json_dumps = jsonlib.dumps
        json_loads = jsonlib.loads
