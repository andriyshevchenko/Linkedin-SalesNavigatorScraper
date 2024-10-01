import asyncio
import logging
import os
import platform

from telegram import Bot

from app.env import EnvLinux, EnvWindows
from app.journal import JrnTelegram
from app.scripts import ScrLogin
from puzzles.core import StrLiteral
from puzzles.journal import JrnByLevel, LvlDefault


async def main():

    log = JrnByLevel(
        JrnTelegram(
            Bot(token=os.environ["ENV_TELEGRAM_BOT_TOKEN"]),
            StrLiteral(os.environ["ENV_TELEGRAM_CHAT_ID"]),
        ),
        LvlDefault(logging.DEBUG),
    )

    await log.write(
        StrLiteral("Successfully started function"), LvlDefault(logging.DEBUG)
    )

    if platform.system() == "Windows":
        driver = await EnvWindows(log).run()
    else:
        driver = await EnvLinux(log).run()

    await log.write(StrLiteral("Driver installed"), LvlDefault(logging.DEBUG))
    await ScrLogin(driver, log).run()
    await driver.close()
    await log.write(StrLiteral("Function quit"), LvlDefault(logging.DEBUG))


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
