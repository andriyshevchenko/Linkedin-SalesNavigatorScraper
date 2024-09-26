"""
Cached String.
"""

from core import String


# pylint: disable=too-few-public-methods
class StrCached(String):
    """
    Cached String.
    """

    value: str
    has_value: bool

    def __init__(self, target: String):
        """
        Initializes a StrCached instance.

        :param target: The String to cache.
        """
        self.target = target
        self.has_value = False

    async def which(self) -> str:
        if not self.has_value:
            self.value = await self.target.which()
            self.has_value = True
        return self.value
