from puzzles.core import String
from puzzles.scraping import Native


class StrNativeDesc(String):
    """
    Reads description from a DOM element.
    """

    def __init__(self, element: Native):
        self.element = element

    async def which(self) -> String:
        return await self.element.which()
