import asyncio
import logging
import os
import platform

from telegram import Bot

from Env import *
from Journal import *
from Scripts import *


async def main():
    telegram = LogByLevel(
        TelegramLog(
            Bot(token=os.environ["ENV_TELEGRAM_BOT_TOKEN"]),
            os.environ["ENV_TELEGRAM_CHAT_ID"],
            os.environ["ENV_FUNCTION_NAME"],
        ),
        logging.DEBUG,
    )
    async with ScopedLog(telegram) as log:
        await log.write("Successfully started function", logging.DEBUG)
        if platform.system() == "Windows":
            driver = await WindowsEnv(log).run()
        else:
            if "ENV_DOCKER" in os.environ:
                await log.write("Running from Docker", logging.INFO)
            driver = await LinuxEnv(log).run()

        await log.write("Driver installed", logging.DEBUG)

        await FinalScript(
            AllOf(
                log,
                LoginScript(driver, log),
                SwitchCaseScript(
                    {
                        "disconnect-leads": DisconnectScript(driver, log),
                        "connect-leads": ConnectAllScript(driver, log),
                    },
                    os.environ["ENV_FUNCTION_NAME"],
                    log,
                ),
            ),
            driver,
            log,
        ).perform()
        await log.write("Function quit", logging.DEBUG)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
