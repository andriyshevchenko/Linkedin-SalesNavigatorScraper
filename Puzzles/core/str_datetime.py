"""
Datetime as string.
"""

from core import DateTime, String


# pylint: disable=too-few-public-methods
class StrDatetime(String):
    """
    Datetime as string.
    """

    def __init__(self, target: DateTime, fmt: String):
        """
        Initializes a StrDatetime instance.

        :param target: The datetime to format.
        :param fmt: The format string.
        """
        self.target = target
        self.fmt = fmt

    async def which(self) -> str:
        datetime = await self.target.which()
        return datetime.strftime(await self.fmt.which())
