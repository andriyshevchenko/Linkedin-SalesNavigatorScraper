# pylint: disable=missing-module-docstring
from abc import ABC, abstractmethod


class Level(ABC):
    """
    Defines a log level.
    """

    @abstractmethod
    def which(self) -> str:
        """
        Return a string representation of value.

        :return: String representation of value.

        """

    @abstractmethod
    def contains(self, level: "Level") -> bool:
        """
        Return a boolean value.

        :return: True if current level contains a level provided in an argument

        """
