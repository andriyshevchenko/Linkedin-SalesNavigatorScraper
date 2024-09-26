"""
Is string empty.
"""

from core import Boolean, String


# pylint: disable=too-few-public-methods
class IsEmpty(Boolean):
    """
    Is string empty.
    """

    def __init__(self, target: String):
        """
        Initialises an IsEmpty instance.

        :param target: The target string to check.
        """
        self.target = target

    async def which(self) -> bool:
        return await self.target.which() == ""
