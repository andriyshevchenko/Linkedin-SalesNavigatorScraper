"""
Formatted String.
"""

from core import String


# pylint: disable=too-few-public-methods
class StrFormatted(String):
    """
    Formatted String.
    """

    def __init__(self, str_format: String, **kwargs):
        """
        Initializes a StrFormatted instance.

        :param str_format: The format string.
        :param kwargs: The keyword arguments to pass to the format string.
        """
        self.str_format = str_format
        self.kwargs = kwargs

    async def which(self) -> str:
        fmt = await self.str_format.which()
        return fmt.format(
            {key: await value.which() for key, value in self.kwargs.items()}
        )
