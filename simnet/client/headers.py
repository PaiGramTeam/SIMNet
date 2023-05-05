from httpx import Headers as _Headers

__all__ = ("Headers",)


class Headers(_Headers):
    """An extension of the `httpx.Headers` class that includes additional functionality."""
