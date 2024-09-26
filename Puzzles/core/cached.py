"""
Loosely typed caching decorator.
Instead of spawning a dozen of different decorators
(`CachedText`, `CachedInt`, etc) this class can be used.

Usage:
```python
    Cached(MyClass("string"), 5).my_method()
```
"""

import asyncio
from functools import wraps


# pylint: disable=too-few-public-methods
class Cached:
    """
    Loosely typed caching decorator.
    Instead of spawning a dozen of different decorators
    (`CachedText`, `CachedInt`, etc) this class can be used.

    Usage:
    ```python
        Cached(MyClass("string"), 5).my_method()
    ```
    """

    def __init__(self, instance):
        """
        Initializes a Cached instance.

        :param instance: The instance to decorate.
        """
        self.instance = instance
        self.has_value = False
        self.value = None

    def __getattr__(self, name):
        # Fetch the attribute from the original instance
        attr = getattr(self.instance, name)
        # If it's an async method, wrap it with custom logic
        if asyncio.iscoroutinefunction(attr):

            @wraps(attr)
            async def wrapper(*args, **kwargs):
                if not self.has_value:
                    self.value = await attr(*args, **kwargs)
                    self.has_value = True
                return self.value

            return wrapper

        # If it's a sync method or other attribute, return as is
        return attr
