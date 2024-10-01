# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod


class Button(ABC):
    """
    Defines anything that can be clicked or interacted with.
    """

    @abstractmethod
    async def click(self):
        """
        Click the button.

        :return: None
        """
