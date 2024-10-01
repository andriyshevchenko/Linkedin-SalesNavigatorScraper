"""
Represents a `Native` decorator which ensures that the element
is present in the DOM.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

from puzzles.core import String
from puzzles.scraping import Native


# pylint: disable=too-few-public-methods
class NtFocused(Native):
    """
    Represents a `Native` decorator which ensures that the element
    is currently in the focus
    """

    def __init__(self, native: Native, driver):
        self.native = native
        self.driver = driver

    async def element(self) -> WebElement:
        element = await self.native.element()
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        return element

    async def which(self) -> String:
        return self.native.which()
