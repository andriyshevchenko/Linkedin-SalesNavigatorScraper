import asyncio
import logging

from Log import ErrorLog

class SafeScript:
    def __init__(self, script, driver, log):
        self.script = script
        self.driver = driver
        self.log = log
    
    async def perform(self) -> str:
        try:
            return await self.script.perform(self.log)
        except asyncio.CancelledError:
            await self.log.write('Job was cancelled', logging.WARNING)
            raise
        except Exception as error:
            await self.log.write(f'Error in Script {self.script.describe()}: \n\n{ErrorLog(error)}', logging.ERROR)