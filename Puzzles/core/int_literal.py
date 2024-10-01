# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.integer import Integer


class IntLiteral(Integer):
    """
    Integer literal.
    """

    def __init__(self, value: int):
        """
        Initialises an IntLiteral instance.

        :param value: Int value of the instance.
        """
        self.value = value

    def which(self) -> int:
        return self.value
