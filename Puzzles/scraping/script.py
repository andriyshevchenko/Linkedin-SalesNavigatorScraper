# pylint: disable=missing-module-docstring

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Script(ABC):
    """
    Defines a script (login, search, etc.).
    """

    @abstractmethod
    async def run(self) -> None:
        """
        Run this script.

        :return: None
        """
