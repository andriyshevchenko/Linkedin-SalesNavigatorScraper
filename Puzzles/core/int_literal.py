"""
Integer literal.
"""

from core import Integer


# pylint: disable=too-few-public-methods
class IntLiteral(Integer):
    """
    Integer literal.
    """

    def __init__(self, value: int):
        """
        Initialises an IntLiteral instance.

        :param value: The int value of the instance.
        """
        self.value = value

    async def which(self) -> int:
        return self.value
