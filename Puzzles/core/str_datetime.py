# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from puzzles.core.datetime import DateTime
from puzzles.core.string import String


class StrDatetime(String):
    """
    Datetime as string.
    """

    def __init__(self, target: DateTime, fmt: String):
        """
        Initializes a `StrDatetime` instance.

        :param target: The datetime to format.
        :param fmt: The format string.
        """
        self.target = target
        self.fmt = fmt

    def which(self) -> str:
        datetime = self.target.which()
        return datetime.strftime(self.fmt.which())
