"""
Defines an empty string.
"""

from core import String


# pylint: disable=too-few-public-methods
class StrEmpty(String):
    """
    Defines an empty string.
    """

    async def which(self) -> str:
        return ""
