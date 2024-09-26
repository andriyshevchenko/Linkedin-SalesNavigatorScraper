"""
String literal.
"""

from core import String


# pylint: disable=too-few-public-methods
class StrLiteral(String):
    """
    String literal.
    """

    def __init__(self, value: str):
        """
        Initializes a StrLiteral instance.

        :param value: The string value of the instance.
        """
        self.value = value

    async def which(self) -> str:
        return self.value
