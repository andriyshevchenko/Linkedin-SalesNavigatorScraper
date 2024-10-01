# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod


class Boolean(ABC):
    """
    Anything that evaluates as True or False.
    """

    @abstractmethod
    def which(self) -> bool:
        """
        Return a boolean value

        :return: a boolean value of the object.
        """
