import asyncio
import logging

class ScopedLog:
    strings = []
    
    def __init__(self, log):
        self.target = log

    async def __aenter__(self):
        self.strings = []
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.target.write('\n'.join(self.strings), logging.CRITICAL)

    async def write(self, text, level):
        self.strings.append(text)    