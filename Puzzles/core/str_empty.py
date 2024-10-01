# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.string import String


class StrEmpty(String):
    """
    An empty string.
    """

    def which(self) -> str:
        return ""
