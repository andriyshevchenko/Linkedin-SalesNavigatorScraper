import logging
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from ErrorLog import ErrorLog
import asyncio

class LoginScript:
    def __init__(self, driver, log):
        self.driver = driver
        self.log = log

    async def perform(self):
        try:
            await self.log.write('Logging user in', logging.INFO)
            self.driver.get('https://www.linkedin.com/sales')
            self.driver.maximize_window()

            await self.log.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)
            time.sleep(random.uniform(5.0, 10.0))

            await self.log.write('Typing email and password', logging.DEBUG)
            username = WebDriverWait(driver=self.driver, timeout=60).until(
               EC.presence_of_element_located((By.ID,'username'))
            )
            username.send_keys(os.environ['ENV_LINKEDIN_USERNAME'])  # Insert your e-mai
            password = WebDriverWait(driver=self.driver, timeout=60).until(
                EC.presence_of_element_located((By.ID,'password'))
            )
            password.send_keys(os.environ['ENV_LINKEDIN_PASSWORD'])  # Insert your password her
            log_in_button = WebDriverWait(driver=self.driver, timeout=60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="btn__primary--large from__button--floating"'))
            )

            await self.log.write(f'Waiting berween 5 and 10 seconds', logging.DEBUG)
            time.sleep(random.uniform(5.0, 10.0))

            await self.log.write('Pressing login button', logging.DEBUG)
            log_in_button.click()

            await self.log.write(f'Waiting 60 seconds', logging.DEBUG)
            time.sleep(60)

            self.driver.switch_to.window(self.driver.current_window_handle)
        except asyncio.CancelledError:
            await self.log.write('Job was cancelled', logging.WARNING)
            raise
        except Exception as error:
            await self.log.write(f'Login error: \n\n{ErrorLog(error)}', logging.ERROR)
            raise