"""
Represents a `Native` decorator which ensures that the element
is present in the DOM.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from puzzles.scraping import Native


# pylint: disable=too-few-public-methods
class NtConfirmed(Native):
    """
    Represents a `Native` decorator which ensures that the element
    is present in the DOM.
    """

    def __init__(self, locator, selector, driver):
        """
        Initialises a NtWaiting instance.

        :param locator: The By-like object.
        :param selector: The selector string.
        :param driver: The Selenium WebDriver instance.
        """
        self.driver = driver
        self.locator = locator
        self.selector = selector

    async def element(self) -> WebElement:
        locator = await self.locator.which()
        selector = await self.selector.which()
        return WebDriverWait(driver=self.driver, timeout=60).until(
            EC.element_to_be_clickable((locator, selector))
        )
