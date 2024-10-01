# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.boolean import Boolean
from puzzles.core.integer import Integer


class BoolGt(Boolean):
    """
    Greater than.
    """

    def __init__(self, a: Integer, b: Integer):
        """
        Initializes a `BoolGt` instance.

        :param target: A left operand.
        :param func: A right operand.
        """
        self.a = a
        self.b = b

    def which(self) -> bool:

        return self.a.which() > self.b.which()
