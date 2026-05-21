import telebot
import requests
from urllib3.exceptions import InsecureRequestWarning

import config
import database.db_manager as db
from handlers.commands import register_handlers
from handlers.messages import register_message_handlers

old_request = requests.Session.request
def new_request(*args, **kwargs):
    kwargs['verify'] = False
    return old_request(*args, **kwargs)
requests.Session.request = new_request

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# ------------------------------------------

db.init_db()

bot = telebot.TeleBot(config.BOT_TOKEN)

register_handlers(bot)
register_message_handlers(bot)

if __name__ == "__main__":
    print("🚀 Student Assistant Bot is running smoothly...")
    bot.infinity_polling()