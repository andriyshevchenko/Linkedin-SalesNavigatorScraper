"""
Defines anything that can be reporesented as text.
"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class String(ABC):
    """
    Defines anything that can be reporesented as text.
    """

    @abstractmethod
    async def which(self) -> str:
        """
        Return a `str` value.

        :return: a `str` value of the object.

        """
