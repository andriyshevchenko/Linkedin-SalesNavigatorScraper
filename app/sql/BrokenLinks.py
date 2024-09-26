import logging


class BrokenLinks:
    def __init__(self, connection, log):
        self.connection = connection
        self.log = log

    async def add(self, link):
        await self.log.write('Inserting into broken profiles table', logging.DEBUG)
        async with self.connection.transaction():
            # Call stored procedure to insert into "broken_links" table
            await self.connection.execute('INSERT INTO broken_linkedin_profiles (profile_url) VALUES ($1) ON CONFLICT DO NOTHING', await link.profile_url())