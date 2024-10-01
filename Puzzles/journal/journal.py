# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod

from puzzles.core.string import String
from puzzles.journal.level import Level


class Journal(ABC):
    """
    Defines a journal (log, logger, notebook etc.)
    """

    @abstractmethod
    async def write(self, message: String, level: Level):
        """
        Writes a message to the journal.

        :param message: The message to write.
        :param level: Severity level.
        :return: None
        """
