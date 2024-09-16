class CachedLink:
    def __init__(self, target):
        self.target = target

    async def profile_url(self):
        if self.link is None:
            self.link = await self.target.profile_url()
        return self.link