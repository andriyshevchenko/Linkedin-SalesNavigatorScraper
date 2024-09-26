import logging

class AlreadyConnectedLinks:
    def __init__(self, connection, log):
        self.connection = connection
        self.log = log

    def links(self):
        return []

    async def add(self, link, full_name):
        await self.log.write(f'Inserting into connected profiles table', logging.DEBUG)
        async with self.connection.transaction():
            # Call stored procedure to insert into "already_connected_profiles" table
            await self.connection.execute('INSERT INTO already_connected_profiles (profile_url, full_name) VALUES ($1, $2) ON CONFLICT DO NOTHING', await link.profile_url(), full_name)
