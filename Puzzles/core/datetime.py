# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
from datetime import datetime


class DateTime(ABC):
    """
    Anything that can evalute to `datetime`.
    """

    @abstractmethod
    def which(self) -> datetime:
        """
        Return a `datetime` value.

        :return: an `datetime` value of the object.

        """
