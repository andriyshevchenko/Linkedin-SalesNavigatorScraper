"""
Anything that evaluates as True or False.
"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Boolean(ABC):
    """
    Anything that evaluates as True or False.
    """

    @abstractmethod
    async def which(self) -> bool:
        """
        Return the boolean value

        :return: the boolean value of the object.
        """
