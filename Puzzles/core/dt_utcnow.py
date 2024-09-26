"""
Current UTC datetime.
"""

from datetime import datetime, timezone

from core import DateTime


# pylint: disable=too-few-public-methods
class DtUtcnow(DateTime):
    """
    Current UTC datetime.
    """

    async def which(self) -> datetime:
        return datetime.now(timezone.utc)
