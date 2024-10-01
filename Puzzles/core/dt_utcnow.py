# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
from datetime import datetime, timezone

from puzzles.core.datetime import DateTime


class DtUtcnow(DateTime):
    """
    Current UTC datetime.
    """

    def which(self) -> datetime:
        return datetime.now(timezone.utc)
