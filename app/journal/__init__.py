"""
Defines a journal (logging) package.
"""

from .jrn_telegram import JrnTelegram
from .jrn_scoped import JrnScoped

__all__ = ["JrnTelegram", "JrnScoped"]
