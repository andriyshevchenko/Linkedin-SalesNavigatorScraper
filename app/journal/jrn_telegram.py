"""
Writes journal messages to a Telegram chat.
"""

from telegram import Bot

from puzzles.core import String
from puzzles.journal import Journal, Level


# pylint: disable=too-few-public-methods
class JrnTelegram(Journal):
    """
    Writes journal messages to a Telegram chat.
    """

    def __init__(self, bot: Bot, chat_id: String):
        self.bot = bot
        self.chat_id = chat_id

    async def write(self, message: String, level: Level):
        await self.bot.send_message(self.chat_id.which(), message.which())
