class SwitchCaseScript:
    def __init__(self, scripts, script_name, log):
        self.scripts = scripts
        self.script_name = script_name
        self.log = log

    async def perform(self):
        await self.scripts[self.script_name].perform(self.log)
