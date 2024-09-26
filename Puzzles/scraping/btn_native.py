"""
Wrapper around selenium DOM element.
"""

from selenium.webdriver.common.action_chains import ActionChains

from puzzles.scraping import Button, Native


# pylint: disable=too-few-public-methods
class BtnNative(Button):
    """
    Wrapper around selenium DOM element.
    """

    def __init__(self, native: Native, driver):
        """
        Initialises a BtnNative instance.

        :param element: The selenium WebElement.
        :param driver: The Selenium WebDriver instance.
        """
        self.native = native
        self.driver = driver

    async def click(self):
        action = ActionChains(self.driver)
        action.move_to_element(await self.native.element()).click().perform()
