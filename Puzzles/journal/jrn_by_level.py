"""
Writes a message to journal only if level specified contains
a level provided in an argument.
"""

from puzzles.core import String
from puzzles.journal import Journal, Level


# pylint: disable=too-few-public-methods
class JrnByLevel(Journal):
    """
    Writes a message to journal only if level specified contains
    a level provided in an argument.
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
            await self.target.write(await message.which(), level)
