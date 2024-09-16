import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WaitFor:
    def __init__(self, selector, driver, log):
        self.selector = selector
        self.driver = driver
        self.log = log

    async def perform(self):
        await self.log.write(f'Waiting for "{self.selector}" to appear', logging.DEBUG)
        WebDriverWait(driver=self.driver, timeout=60).until(
            EC.presence_of_element_located((By.XPATH, './/button[@aria-label="More actions"]')))  
        return 'Waited'