# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod


class String(ABC):
    """
    Defines anything that can be reporesented as text.
    """

    @abstractmethod
    def which(self) -> str:
        """
        Return a `str` value.

        :return: a `str` value of the object.

        """
