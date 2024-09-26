"""
Greater than.
"""

from core import Boolean, Integer


# pylint: disable=too-few-public-methods
class Gt(Boolean):
    """
    Greater than.
    """

    def __init__(self, a: Integer, b: Integer):
        """
        Initializes a Gt instance.

        :param target: The left operand.
        :param func: The right operand.
        """
        self.a = a
        self.b = b

    async def which(self) -> bool:

        return await self.a.which() > await self.b.which()
