# my_package/__init__.py

from .env_linux import EnvLinux
from .env_windows import EnvWindows

# Define the public API for the module
__all__ = ["env_linux", "env_windows"]
