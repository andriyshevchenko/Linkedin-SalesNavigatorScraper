class SequentialScript:
    def __init__(self, log, *scripts):
        self.scripts = scripts
        self.log = log
    
    async def perform(self):
        for script in self.scripts:
            await script.perform(self.log)