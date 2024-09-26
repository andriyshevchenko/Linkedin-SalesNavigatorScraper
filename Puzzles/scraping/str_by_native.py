"""
Reads text from a DOM element.
"""

from puzzles.core import String
from puzzles.scraping import Native


# pylint: disable=too-few-public-methods
class StrByNative(String):
    """
    Reads text from a DOM element.
    """

    def __init__(self, element: Native):
        self.element = element

    async def which(self) -> str:
        return self.element.text.strip()
