"""
Anything that can evalute to `datetime`.
"""

from abc import ABC, abstractmethod
from datetime import datetime


# pylint: disable=too-few-public-methods
class DateTime(ABC):
    """
    Anything that can evalute to `datetime`.
    """

    @abstractmethod
    async def which(self) -> datetime:
        """
        Return a `datetime` value.

        :return: an `datetime` value of the object.

        """
