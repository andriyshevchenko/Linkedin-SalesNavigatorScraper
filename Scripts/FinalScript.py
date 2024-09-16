import logging

class FinalScript:
    def __init__(self, script, driver, log):
        self.script = script
        self.driver = driver
        self.log = log
    
    async def perform(self) -> str:
        try:
            return await self.script.perform(self.log)
        except:
            raise
        finally:
            await self.log.write('Cleaning Selenium resources', logging.INFO)
            self.driver.quit()