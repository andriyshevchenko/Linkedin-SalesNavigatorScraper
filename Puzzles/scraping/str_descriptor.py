from puzzles.core import StrFormatted, String, StrLiteral


class StrDescriptor(StrFormatted):
    def __init__(self, selector: String, locator: String):
        super().__init__(
            StrLiteral("By.{locator}:'{selector}'"),
            kwargs={"locator": locator, "selector": selector},
        )
