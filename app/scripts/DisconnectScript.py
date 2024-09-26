import logging
import random
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Journal import ErrorLog

from . import Script


class DisconnectScript(Script):
    def __init__(self, driver, log):
        self.driver = driver
        self.log = log

    async def run(self):
        self.driver.get("https://www.linkedin.com/mynetwork/invitation-manager/sent/")
        time.sleep(random.uniform(5.0, 10.0))
        self.perform_scroll_to_bottom(self.driver)
        pages = ["https://www.linkedin.com/mynetwork/invitation-manager/sent?page=1"]
        number_pages = 1
        try:
            WebDriverWait(driver=self.driver, timeout=60).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        './/ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]',
                    )
                )
            )
            number_pages = len(
                list(
                    self.driver.find_elements(
                        By.XPATH,
                        './/ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]/descendant::li',
                    )
                )
            )
            pages = list(
                map(
                    lambda number: f"https://www.linkedin.com/mynetwork/invitation-manager/sent?page={number}",
                    range(1, number_pages + 1),
                )
            )
        except:
            pass
        await self.log.write(
            f"There are {number_pages} pages. Withdrawing requests...", logging.DEBUG
        )
        for page in pages:
            self.driver.get(page)
            time.sleep(random.uniform(5.0, 10.0))
            try:
                self.perform_scroll_to_bottom(self.driver)
                time.sleep(random.uniform(5.0, 10.0))
                buttons = self.driver.find_elements(
                    By.XPATH,
                    '(.//span[contains(.,"weeks") or contains(.,"month") or contains(.,"months")])/following::button[@class="artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view invitation-card__action-btn"][1]',
                )
                for button in buttons:
                    action = ActionChains(self.driver)
                    # perform the operation
                    action.move_to_element(button).click().perform()
                    time.sleep(random.uniform(5.0, 10.0))
                    submit_button = WebDriverWait(driver=self.driver, timeout=60).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                './/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view artdeco-modal__confirm-dialog-btn"]',
                            )
                        )
                    )
                    submit_button.click()
                time.sleep(random.uniform(5.0, 10.0))
                await self.log.write(
                    f"Withdrawn {len(buttons)} requests", logging.DEBUG
                )
            except Exception as error:
                await self.log.write(
                    f"Problem encontered: {ErrorLog(error)}", logging.DEBUG
                )

    def perform_scroll_to_bottom(self):
        height: int = 0
        while height < self.driver.execute_script("return document.body.scrollHeight"):
            height += 20
            self.driver.execute_script("window.scrollTo(0, {});".format(height))
            time.sleep(0.0125)
