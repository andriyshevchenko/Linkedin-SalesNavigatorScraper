# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods

from puzzles.core.string import String
from puzzles.journal.journal import Journal
from puzzles.journal.level import Level


class JrnByLevel(Journal):
    """
    Writes a message to journal only if level specified contains
    a level provided in an argument. For example, level 'DEBUG'
    contains 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
    """

    def __init__(self, log: Journal, level: Level):
        """
        Initializes an instance of JrnByLevel.

        :param log: The Journal to decorate.
        :param level: Base log level.
        """
        self.target = log
        self.level = level

    async def write(self, message: String, level: Level):
        if self.level.contains(level):
            await self.target.write(message, level)
