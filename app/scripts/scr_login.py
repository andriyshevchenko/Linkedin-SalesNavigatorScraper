import asyncio
import logging
import os
import random

from puzzles.core import StrLiteral
from puzzles.journal import LvlDefault
from puzzles.scraping import Script


class ScrLogin(Script):
    def __init__(self, driver, log):
        self.driver = driver
        self.log = log

    async def run(self):
        await self.log.write(
            StrLiteral("Logging user in"), LvlDefault(logging.INFO)
        )
        await self.driver.goto("https://www.linkedin.com/sales")
        await self.driver.set_viewport_size({"width": 1920, "height": 1080})

        await self.log.write(
            StrLiteral("Waiting between 5 and 10 seconds"),
            LvlDefault(logging.DEBUG)
        )
        await asyncio.sleep(random.uniform(5.0, 10.0))

        await self.log.write(
            StrLiteral("Typing email and password"), LvlDefault(logging.DEBUG)
        )
        username = await self.driver.wait_for_selector("#username",
                                                       timeout=60000)
        await username.fill(os.environ["ENV_LINKEDIN_USERNAME"])

        password = await self.driver.wait_for_selector("#password",
                                                       timeout=60000)
        await password.fill(os.environ["ENV_LINKEDIN_PASSWORD"])

        log_in_button = await self.driver.wait_for_selector(
            "button.btn__primary--large.from__button--floating",
            timeout=60000
        )

        await self.log.write(
            StrLiteral("Waiting between 5 and 10 seconds"),
            LvlDefault(logging.DEBUG)
        )
        await asyncio.sleep(random.uniform(5.0, 10.0))

        await self.log.write(
            StrLiteral("Pressing login button"), LvlDefault(logging.DEBUG)
        )
        await log_in_button.click()

        await self.log.write(
            StrLiteral("Waiting 60 seconds"), LvlDefault(logging.DEBUG)
        )
        await asyncio.sleep(60)
        await self.driver.bring_to_front()
