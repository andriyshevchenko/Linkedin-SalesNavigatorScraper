"""
Prints an exception's stack trace in a human readable format.
"""

import sys

# mypy: disable-error-code="import-untyped"
import better_exceptions

from puzzles.core import String


class StrByException(String):
    """
    Prints an exception's stack trace in a human readable format.
    """

    def __init__(self, exception):
        """
        Initialises a StrByException instance.

        :param exception: Exception object.
        """
        self.exception = exception

    async def which(self):
        exc_type, exc_value, exc_tb = sys.exc_info()
        return "\n".join(
            better_exceptions.format_exception(exc_type, exc_value, exc_tb)
        )
