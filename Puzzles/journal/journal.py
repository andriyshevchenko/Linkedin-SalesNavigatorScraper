"""
Defines a notebook (log, logger, report etc.)
"""

from abc import ABC, abstractmethod

from puzzles.core import String
from puzzles.journal import Level


# pylint: disable=too-few-public-methods
class Journal(ABC):
    """
    Defines a notebook (log, logger, report etc.)
    """

    @abstractmethod
    async def write(self, message: String, level: Level):
        """
        Writes a message to the journal.

        :param message: The message to write.
        :param level: The level of the message.
        :return: None
        """
