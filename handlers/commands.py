from telebot import types
import database.db_manager as db

def register_handlers(bot):
    
    # 1. /start command - Welcome & Main Menu
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        db.add_user(message.from_user.id, message.from_user.username)
        
        # Main Reply Keyboard
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("📚 Cheatsheets")
        btn2 = types.KeyboardButton("📝 My Tasks")
        btn3 = types.KeyboardButton("🗺️ Almaty Locations")
        btn4 = types.KeyboardButton("🇬🇧 English Boost")
        btn5 = types.KeyboardButton("🧮 Calculator")
        btn6 = types.KeyboardButton("ℹ️ Help")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        
        bot.send_message(
            message.chat.id, 
            f"Hello, {message.from_user.first_name}! 👋\nI am your smart Student Assistant Bot. Choose an option below:", 
            reply_markup=markup
        )

    # 2. /help command or Help button
    @bot.message_handler(commands=['help'])
    @bot.message_handler(func=lambda msg: msg.text == "ℹ️ Help")
    def send_help(message):
        help_text = (
            "🤖 **Available Bot Commands:**\n\n"
            "/start — Restart the bot and open main menu\n"
            "/help — Show this help message\n"
            "/tasks — View your current task list\n"
            "/clear — Delete all tasks from your list\n"
            "/about — Learn more about this project\n\n"
            "Use the interactive keyboard buttons to access formulas, English idioms, "
            "the expression calculator, and the Almaty student guide!"
        )
        bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

    # 3. /about command
    @bot.message_handler(commands=['about'])
    def send_about(message):
        bot.send_message(
            message.chat.id, 
            "📐 *Project:* Student Assistant Bot\n"
            "🚀 *Version:* 1.0\n"
            "🎯 *Purpose:* Final project for the 'Python Programming' course.\n"
            "The bot helps students track tasks, study core materials, and perform quick math calculations.",
            parse_mode="Markdown"
        )

    # 4. View tasks via command /tasks
    @bot.message_handler(commands=['tasks'])
    def show_tasks_cmd(message):
        user_tasks = db.get_tasks(message.from_user.id)
        if not user_tasks:
            bot.send_message(message.chat.id, "📭 Your task list is empty. Click '📝 My Tasks' to add a new one.")
        else:
            response = "📋 *Your Current Tasks:*\n\n" + "\n".join([f"• {task}" for task in user_tasks])
            bot.send_message(message.chat.id, response, parse_mode="Markdown")

    # 5. Clear tasks via command /clear
    @bot.message_handler(commands=['clear'])
    def clear_tasks_cmd(message):
        db.clear_tasks(message.from_user.id)
        bot.send_message(message.chat.id, "🗑️ All your tasks have been successfully deleted from the database.")