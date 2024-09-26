"""
Determine if a page has certain element.
"""

from puzzles.core import Boolean, String


# pylint: disable=too-few-public-methods
class BoolHasElement(Boolean):
    """
    Determine if a page has certain element.
    """

    def __init__(self, selector: String, locator: String, driver):
        """
        Initialises a BoolHasElement instance.

        :param selector: The selector string.
        :param locator: The By-like object.
        :param driver: The Selenium WebDriver instance.
        """
        self.selector = selector
        self.locator = locator
        self.driver = driver

    async def which(self) -> bool:
        locator = await self.locator.which()
        selector = await self.selector.which()
        elements = self.driver.find_elements(locator, selector)
        return len(elements) > 0
