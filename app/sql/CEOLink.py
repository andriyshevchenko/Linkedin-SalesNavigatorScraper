import logging


class CEOLink:
    def __init__(self, connection, log):
        self.connection = connection
        self.log = log

    async def profile_url(self):
        await self.log.write("Reading next CEO profile_url", logging.DEBUG)
        row = await self.connection.fetchrow(
            """
            WITH select_ceo AS (
                SELECT pp.profile_url, pp.full_name
                FROM connected_profiles pp
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

            SELECT * FROM select_ceo;
        """
        )
        return row["profile_url"]
