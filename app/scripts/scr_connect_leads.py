from asyncpg import Connection

from app.sql import (
    AlreadyConnectedLink,
    ArchitectLink,
    BrokenLink,
    CachedLink,
    CEOLink,
    LinkList,
    RandomLink,
)
from puzzles.journal import Journal
from puzzles.scraping import Script


class ScrConnectLeads(Script):

    def __init__(self, driver, log: Journal, connection: Connection):
        self.driver = driver
        self.log = log
        self.connection = connection

    async def perform(self) -> None:
        already_connected = AlreadyConnectedLinks(connection, self.log)
        broken = BrokenLinks(connection, self.log)

        links = LinkList(
            connection,
            lambda: CachedLink(
                RandomLink(
                    [ArchitectLink(connection, self.log), CEOLink(connection, self.log)]
                )
            ),
            int(os.environ["ENV_MAX_ALLOWED_CONNECTION_REQUESTS"]),
            self.log,
        )
