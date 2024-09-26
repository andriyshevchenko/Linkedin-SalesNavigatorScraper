"""
Defines anything that can be clicked.
"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Button(ABC):
    """
    Defines anything that can be clicked.
    """

    @abstractmethod
    async def click(self):
        """
        Click the button.

        :return: None
        """
