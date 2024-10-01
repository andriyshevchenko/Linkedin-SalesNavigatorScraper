# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods

import asyncio

from puzzles.core import Integer
from puzzles.scraping import Button


class BtnDeferred(Button):

    def __init__(self, button: Button, seconds_wait: Integer):
        self.button = button
        self.seconds_wait = seconds_wait

    async def click(self):
        await asyncio.wait(self.seconds_wait)
        await self.button.click()
