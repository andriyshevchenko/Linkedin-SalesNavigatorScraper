# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod


class Integer(ABC):
    """
    Anything that can evalute to `int`.
    """

    @abstractmethod
    def which(self) -> int:
        """
        Returns an `int` value.

        :return:`int` value of the object.

        """
