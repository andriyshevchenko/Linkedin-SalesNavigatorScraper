# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.string import String


class StrFormatted(String):
    """
    Formatted String.
    """

    def __init__(self, str_format: String, **kwargs):
        """
        Initializes a StrFormatted instance.

        :param str_format: Format string.
        :param kwargs: Keyword arguments to pass to the format string.
        """
        self.str_format = str_format
        self.kwargs = kwargs

    def which(self) -> str:
        fmt = self.str_format.which()
        return fmt.format(
            {key: value.which() for key, value in self.kwargs.items()}
        )
