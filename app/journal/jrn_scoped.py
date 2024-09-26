"""
Aggregates logs until we leave current scope.
Usage:
```python
    async with JrnScoped(target):
```
"""

import logging

from puzzles.core import String
from puzzles.journal import Journal, Level, LvlPython


class JrnScoped(Journal):
    """
    Aggregates logs until we leave current scope.
    Usage:
    ```python
        async with JrnScoped(target):
    ```
    """

    strings: list[String]
    level: Level

    def __init__(self, log: Journal):
        
        self.strings = []
        self.log = log
        self.level = LvlPython(logging.CRITICAL)

    async def __aenter__(self):
        self.strings = []
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.log.write("\n".join(self.strings), self.level)

    async def write(self, message, level):
        self.strings.append(message)
        if level.contains(self.level):
            self.level = level
