"""
Represents a `Native` decorator which will explicitly
wait before running the code.
"""

from selenium.webdriver.remote.webelement import WebElement

from puzzles.core import String
from puzzles.scraping import Native
from puzzles.scraping.str_descriptor import StrDescriptor


# pylint: disable=too-few-public-methods
class NtSelector(Native):
    """
    Represents an element queried from the DOM.
    """

    def __init__(self, driver, locator: String, selector: String):
        """
        Initialises a NtSelector instance.

        :param driver: The Selenium WebDriver instance.
        :param locator: The By-like object.
        :param selector: The selector string.
        """
        self.driver = driver
        self.locator = locator
        self.selector = selector
        self.name = StrDescriptor(selector, locator)

    async def element(self) -> WebElement:
        selector = await self.selector.which()
        locator = await self.locator.which()
        return self.driver.find_element(locator, selector)

    async def which(self) -> String:
        return self.which
