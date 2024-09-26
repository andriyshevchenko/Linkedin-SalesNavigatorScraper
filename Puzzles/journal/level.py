"""
Defines a log level.
"""

from abc import ABC, abstractmethod


class Level(ABC):
    """
    Defines a log level.
    """

    @abstractmethod
    def which(self) -> str:
        """
        Return a string representation of value.

        :return: string representation of value.

        """

    @abstractmethod
    def contains(self, level: "Level") -> bool:
        """
        Return a boolean value.

        :return: None a boolean value of the object.

        """
