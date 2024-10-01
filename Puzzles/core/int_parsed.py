# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.integer import Integer
from puzzles.core.string import String


class IntParsed(Integer):
    """
    Parses an `Integer` from `String`.
    """

    def __init__(self, value: String):
        """
        Initializes an IntParsed instance.

        :param value: A `String` to parse.
        """
        self.value = value

    def which(self) -> int:
        return int(self.which())
