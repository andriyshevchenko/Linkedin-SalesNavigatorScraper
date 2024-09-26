"""
Parses an `Integer` from `String`.
"""

from core import Integer, String


# pylint: disable=too-few-public-methods
class IntParsed(Integer):
    """
    Parses an `Integer` from `String`.
    """

    def __init__(self, value: String):
        """
        Initializes an IntParsed instance.

        :param value: The String to parse.
        """
        self.value = value

    async def which(self) -> int:
        return int(await self.which())
