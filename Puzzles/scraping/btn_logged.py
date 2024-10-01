import asyncio
import logging

from puzzles.core import StrFormatted, StrLiteral
from puzzles.journal import Journal, LvlDefault
from puzzles.scraping import Button, Native, StrNativeDesc


class BtnLogged(Button):
    def __init__(self, native: Native, journal: Journal):
        self.native = native
        self.journal = journal
        self.message = StrFormatted(
            StrLiteral("Clicking button {0}"),
            kwargs={"btn": StrNativeDesc(native)}
        )
        self.level = LvlDefault(logging.DEBUG)
  
    async def click(self):
        await asyncio.gather(
            self.journal.write(self.message, self.level),
            self.native.click(),
            return_exceptions=False,
        )
