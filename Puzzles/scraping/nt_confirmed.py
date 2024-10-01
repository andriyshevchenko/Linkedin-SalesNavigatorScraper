"""
Represents a `Native` decorator which ensures that the element
is present in the DOM.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from puzzles.core import String
from puzzles.scraping import Native, StrDescriptor


# pylint: disable=too-few-public-methods
class NtConfirmed(Native):
    """
    Represents a native selenium element which waits
    until it becomes clickable.
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
        self.name = StrDescriptor(selector, locator)

    async def element(self) -> WebElement:
        locator = await self.locator.which()
        selector = await self.selector.which()
        return WebDriverWait(driver=self.driver, timeout=60).until(
            EC.element_to_be_clickable((locator, selector))
        )

    async def which(self) -> String:
        return self.name
