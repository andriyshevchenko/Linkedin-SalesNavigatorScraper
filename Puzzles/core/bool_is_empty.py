# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.boolean import Boolean
from puzzles.core.string import String


class BoolStrEmpty(Boolean):
    """
    Is string empty.
    """

    def __init__(self, target: String):
        """
        Initialises a `BoolStrEmpty` instance.

        :param target: Target string to check.
        """
        self.target = target

    def which(self) -> bool:
        return self.target.which() == ""
