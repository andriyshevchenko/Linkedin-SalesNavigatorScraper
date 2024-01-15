from telegram import Bot
from datetime import datetime, timezone

class NullLog:
    def __init__(self, bot: Bot, chat_id, _function):
        pass
    
    async def write(self, text):
        pass

class TelegramLog:
    def __init__(self, bot: Bot, chat_id, _function):
        self.bot = bot
        self.chat_id = chat_id
        self._function = _function

    async def write(self, text):
        format_string = "%Y-%m-%d %H:%M"
        server_timestamp = datetime.now(timezone.utc).strftime(format_string)
        await self.bot.send_message(self.chat_id, f'Function: {self._function}\nTime: {server_timestamp}\n{text}')