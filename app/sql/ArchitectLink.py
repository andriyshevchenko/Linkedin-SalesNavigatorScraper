import logging

class ArchitectLink:
    def __init__(self, connection, log):
        self.connection = connection
        self.log = log

    async def profile_url(self):
        await self.log.write('Reading next Architect profile_url', logging.DEBUG)
        row = await self.connection.fetchrow("""
            WITH select_architect AS (
                SELECT pp.profile_url, pp.full_name
                FROM architect_linkedin_profiles pp
                WHERE pp.profile_url NOT IN (
                    SELECT profile_url FROM already_connected_profiles
                    UNION ALL
                    SELECT profile_url FROM broken_linkedin_profiles
                    UNION ALL
                    SELECT sales_navigator_profile_url FROM broken_links
                )
                ORDER BY random()
                LIMIT 1
            )

            SELECT * FROM select_architect;
        """
        )
        return row['profile_url']