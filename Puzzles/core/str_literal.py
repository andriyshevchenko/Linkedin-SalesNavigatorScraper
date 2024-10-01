# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.string import String


class StrLiteral(String):
    """
    String literal.
    """

    def __init__(self, value: str):
        """
        Initializes a `StrLiteral` instance.

        :param value: A string value of the instance.
        """
        self.value = value

    def which(self) -> str:
        return self.value
