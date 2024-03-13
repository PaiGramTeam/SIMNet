from typing import NamedTuple

__all__ = ("__version__", "__version_info__")


class Version(NamedTuple):
    """Copies the behavior of sys.version_info. serial is always 0 for stable releases."""

    major: int
    minor: int
    micro: int
    release_level: str
    serial: int

    def _rl_shorthand(self) -> str:  # skipcq: PY-D0003
        return {
            "alpha": "a",
            "beta": "b",
            "candidate": "rc",
        }[self.release_level]

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}"
        if self.micro != 0:
            version = f"{version}.{self.micro}"
        if self.release_level != "final":
            version = f"{version}{self._rl_shorthand()}{self.serial}"

        return version


__version_info__ = Version(major=0, minor=1, micro=21, release_level="beta", serial=0)
__version__ = str(__version_info__)
