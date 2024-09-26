"""
Mapped Async iterator.
"""


class AitMapped:
    """
    Mapped Async iterator. Decorates an existing async iterator
    by applying a function to each item returned by the iterator.
    """

    def __init__(self, target, func):
        """
        Initialises the async iterator.

        :param target: The async iterator to decorate.
        :param func: The function to apply to each item.
        """
        self.target = target
        self.func = func

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            item = await self.target.__anext__()
            return self.func(item)
        except StopAsyncIteration:
            # pylint: disable=raise-missing-from
            raise StopAsyncIteration
