"""
Loosely typed decorator, which will wait before running the code.
Usage:
```python
    Paused(MyClass("string"), 5).my_method()
```
"""

import asyncio
from functools import wraps

from puzzles.core import Integer


# pylint: disable=too-few-public-methods
class Paused:
    """
    Loosely typed decorator, which will wait before running the code.
    Usage:
    ```python
        Paused(MyClass("string"), 5).my_method()
    ```
    """

    def __init__(self, instance, seconds: Integer):
        """
        Initializes a Paused instance.

        :param instance: The instance to decorate.
        :param seconds: The number of seconds to wait before running the code.
        """
        self.instance = instance
        self.seconds = seconds

    def __getattr__(self, name):
        # Fetch the attribute from the original instance
        attr = getattr(self.instance, name)
        # If it's an async method, wrap it with custom logic
        if asyncio.iscoroutinefunction(attr):

            @wraps(attr)
            async def wrapper(*args, **kwargs):
                await asyncio.sleep(self.seconds)
                return await attr(*args, **kwargs)

            return wrapper

        # If it's a sync method or other attribute, return as is
        return attr
