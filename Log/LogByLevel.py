import logging

class LogByLevel:

    def __init__(self, log, level):
        self.target = log
        self.level = level

    async def write(self, text, level):
        if self.level <= level:
            await self.target.write(text, level)   