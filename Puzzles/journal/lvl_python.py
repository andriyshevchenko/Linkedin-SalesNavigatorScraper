"""
Defines a default python logging levels.
"""

import logging

from puzzles.journal import Level


class LvlPython(Level):
    """
    Defines a default python logging levels.
    """

    def __init__(self, value: int):
        """
        Initialises an LvlPython instance.

        :param value: The int value.
        """
        self.value = value
        self.level_to_name = {
            logging.CRITICAL: "CRITICAL",
            logging.ERROR: "ERROR",
            logging.WARNING: "WARNING",
            logging.INFO: "INFO",
            logging.DEBUG: "DEBUG",
            logging.NOTSET: "NOTSET",
        }
        self.name_to_level = {
            "CRITICAL": logging.CRITICAL,
            "FATAL": logging.FATAL,
            "ERROR": logging.ERROR,
            "WARN": logging.WARNING,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "NOTSET": logging.NOTSET,
        }

    def which(self) -> str:
        return self.level_to_name[self.value]

    def contains(self, level: "Level") -> bool:
        return self.value <= self.name_to_level[level.which()]
