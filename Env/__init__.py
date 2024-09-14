# my_package/__init__.py

from .LinuxEnv import LinuxEnv
from .WindowsEnv import WindowsEnv

# Define the public API for the module
__all__ = ['LinuxEnv', 'WindowsEnv']
