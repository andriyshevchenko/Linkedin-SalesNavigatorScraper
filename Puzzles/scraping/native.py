"""
Represents a native selenium element.
"""

from abc import ABC, abstractmethod

from selenium.webdriver.remote.webelement import WebElement


# pylint: disable=too-few-public-methods
class Native(ABC):
    """
    Represents a native selenium element.
    """

    @abstractmethod
    async def element(self) -> WebElement:
        """
        Returns the underlying selenium element.

        :return: None
        """
