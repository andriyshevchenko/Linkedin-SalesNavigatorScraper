# my_package/__init__.py

from .ErrorLog import ErrorLog
from .LogByLevel import LogByLevel
from .ScopedLog import ScopedLog
from .TelegramLog import TelegramLog

# Define the public API for the module
__all__ = ['ErrorLog', 'LogByLevel', 'ScopedLog', 'TelegramLog']
