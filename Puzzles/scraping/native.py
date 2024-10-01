# pylint: disable=missing-module-docstring

from abc import ABC, abstractmethod

from puzzles.core import String


# pylint: disable=too-few-public-methods
class Native(ABC):
    """
    Represents a native web driver element (Selenium, Playwright, etc.).
    """

    @abstractmethod
    async def element(self):
        """
        Returns an underlying web driver element.

        :return: Native web driver element.
        """

    @abstractmethod
    async def which(self) -> String:
        """
        Provides a description of the element.

        :return: A string description identifying the element.
        """
