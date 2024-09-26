"""
Represents a native selenium element.
"""

from selenium.webdriver.remote.webelement import WebElement

from puzzles.scraping import Native


# pylint: disable=too-few-public-methods
class NtLiteral(Native):
    """
    Represents a native selenium element.
    """

    def __init__(self, ref: WebElement):
        """
        Initializes a OrgFromRef instance.

        :param ref: Selenium WebElement.
        """
        self.ref = ref

    async def element(self) -> WebElement:
        return self.ref
