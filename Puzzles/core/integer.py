"""
Anything that can evalute to `int`.
"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Integer(ABC):
    """
    Anything that can evalute to `int`.
    """

    @abstractmethod
    async def which(self) -> int:
        """
        Return an `int` value.

        :return: an `int` value of the object.

        """
