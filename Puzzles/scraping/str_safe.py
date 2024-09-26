"""
String decorator.
If there's  `NoSuchElementException` exception thrown, return an alternative.
"""

from selenium.common.exceptions import NoSuchElementException

from puzzles.core import String


# pylint: disable=too-few-public-methods
class StrSafe(String):
    """
    String decorator.
    If there's `NoSuchElementException` exception thrown,
    return an alternative.
    """

    def __init__(self, target: String, alternative: String):
        self.target = target
        self.alternative = alternative

    async def which(self) -> str:
        try:
            return await self.target.which()
        except NoSuchElementException:
            return await self.alternative.which()
