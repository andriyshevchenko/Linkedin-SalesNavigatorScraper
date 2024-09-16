import random


class RandomLink:
    def __init__(self, targets):
        self.targets = targets

    async def profile_url(self):
        lead = await random.choice(self.targets)
        return await lead.profile_url()