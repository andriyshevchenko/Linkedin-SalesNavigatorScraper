"""
Provides an async iterable interface for a list of
selenium DOM elements.
"""

from puzzles.core import String


class AitSelector:
    """
    Provides an async iterable interface for a list of
    selenium DOM elements.
    """

    def __init__(self, selector: String, locator: String, driver):
        """
        Initialises an AitSelector instance.

        :param selector: The selector string.
        :param locator: The By-like object.
        :param driver: The Selenium WebDriver instance.
        """
        self.selector = selector
        self.locator = locator
        self.driver = driver
        self.index = 0
        self.count = 0
        self.elements = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        locator = await self.locator.which()
        selector = await self.selector.which()
        if self.index == 0:
            self.elements = await self.driver.find_elements(locator, selector)
            self.count = len(self.elements)
        if self.index < self.count:
            element = self.elements[self.index]
            self.index += 1
            return element
        raise StopAsyncIteration
