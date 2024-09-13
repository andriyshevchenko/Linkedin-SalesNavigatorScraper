import logging
import os
import platform
from ConnectScript import ConnectScript
from DisconnectScript import DisconnectScript
from FinalScript import FinalScript
from LinuxEnv import LinuxEnv
from LogByLevel import LogByLevel
from LoginScript import LoginScript
from ScopedLog import ScopedLog
from SequentialScript import SequentialScript
from SwitchCaseScript import SwitchCaseScript
from TelegramLog import TelegramLog
from telegram import Bot
import asyncio
from WindowsEnv import WindowsEnv

async def main():
    telegram = LogByLevel(TelegramLog(Bot(token=os.environ['ENV_TELEGRAM_BOT_TOKEN']), os.environ['ENV_TELEGRAM_CHAT_ID'], os.environ['ENV_FUNCTION_NAME']), logging.DEBUG)  
    async with ScopedLog(telegram) as log:
        await log.write('Successfully started function', logging.DEBUG)
        if platform.system() == "Windows":
            driver = await WindowsEnv(log).run()
        else:
            if 'ENV_DOCKER' in os.environ:
                await log.write('Running from Docker', logging.INFO)
            driver = await LinuxEnv(log).run()
    
        await log.write('Driver installed', logging.DEBUG)
        
        await FinalScript(
            SequentialScript(
                LoginScript(driver, log),
                SwitchCaseScript(
                    {
                        'disconnect-leads': DisconnectScript(driver, log),
                        'connect-leads': ConnectScript(driver, log)
                    },
                    os.environ['ENV_FUNCTION_NAME'],
                    log
                ),
                log
            ),
            driver,
            log).perform()
        await log.write('Function quit', logging.DEBUG)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())