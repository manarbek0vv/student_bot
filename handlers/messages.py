from telebot import types
import database.db_manager as db

def register_message_handlers(bot):

    # Dictionary to keep track of conversation states
    user_states = {}

    @bot.message_handler(content_types=['text'])
    def handle_text_messages(message):
        chat_id = message.chat.id
        text = message.text

        # State check: Waiting for user to type a task
        if user_states.get(chat_id) == 'waiting_for_task':
            if not text.strip():
                bot.send_message(chat_id, "⚠️ Task text cannot be empty. Please try again.")
                return
            db.add_task(message.from_user.id, text)
            user_states[chat_id] = None
            bot.send_message(chat_id, "✅ Task successfully saved to the database!")
            return

        # State check: Waiting for a math expression
        if user_states.get(chat_id) == 'waiting_for_calc':
            user_states[chat_id] = None
            try:
                # Basic input validation for security reasons
                allowed_chars = "0123456789+-*/(). "
                if all(char in allowed_chars for char in text):
                    result = eval(text)
                    bot.send_message(chat_id, f"🔢 *Calculation Result:* `{result}`", parse_mode="Markdown")
                else:
                    bot.send_message(chat_id, "⚠️ Invalid input! You can only use numbers and signs +, -, *, /, (, ).")
            except Exception:
                bot.send_message(chat_id, "❌ Error evaluating the expression. Please check your syntax.")
            return

        # --- MAIN MENU NAVIGATION ---
        
        # 6. Cheatsheets (Inline Buttons)
        if text == "📚 Cheatsheets":
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_math = types.InlineKeyboardButton("📐 Higher Mathematics", callback_data="shpor_math")
            btn_phys = types.InlineKeyboardButton("⚡ Physics (Electrodynamics)", callback_data="shpor_phys")
            markup.add(btn_math, btn_phys)
            bot.send_message(chat_id, "Which subject do you want to review?", reply_markup=markup)

        # 7. My Tasks Menu
        elif text == "📝 My Tasks":
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_view = types.InlineKeyboardButton("👁️ View Tasks", callback_data="tasks_view")
            btn_add = types.InlineKeyboardButton("➕ Add Task", callback_data="tasks_add")
            btn_clear = types.InlineKeyboardButton("🗑️ Clear All", callback_data="tasks_clear")
            markup.add(btn_view, btn_add, btn_clear)
            bot.send_message(chat_id, "Manage your academic tasks:", reply_markup=markup)

        # 8. Almaty Locations Guide
        elif text == "🗺️ Almaty Locations":
            locations = (
                "🏙️ *Top Useful Almaty Locations for Students:*\n\n"
                "1. *Kok-Tobe* — Stunning city views, fresh air, and a cable car ride.\n"
                "2. *Medeu & Shymbulak* — Iconic high-altitude mountain complexes for active rest.\n"
                "3. *Terrenkur* — A perfect, peaceful walking path to revise lectures outdoors.\n"
                "4. *National Library of the RK* — The ultimate quiet spot for focused session prep."
            )
            bot.send_message(chat_id, locations, parse_mode="Markdown")

        # 9. English Boost Collocations
        elif text == "🇬🇧 English Boost":
            phrases = (
                "🗣️ *Essential Academic Collocations:*\n\n"
                "• *Do research* — To conduct a scientific study.\n"
                "• *Meet a deadline* — To finish a task on time.\n"
                "• *Take an exam* — The process of sitting for a test.\n"
                "• *Pass an exam* — Achieving a successful result in a test.\n"
                "• *Make progress* — To develop or improve skills."
            )
            bot.send_message(chat_id, phrases, parse_mode="Markdown")

        # 10. Calculator Input Trigger
        elif text == "🧮 Calculator":
            user_states[chat_id] = 'waiting_for_calc'
            bot.send_message(chat_id, "Please enter a mathematical expression (e.g., `(12 + 8) * 5 / 2`):", parse_mode="Markdown")

        # 11. Fallback for Unknown Requests (Error Handling)
        else:
            bot.send_message(
                chat_id, 
                "🤔 Sorry, I didn't recognize that command or message.\n"
                "Please use the menu buttons or type /help for assistance."
            )

    # --- INLINE BUTTON CALLBACK HANDLERS ---
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        chat_id = call.message.chat.id
        
        # 12. Math Formulas Response
        if call.data == "shpor_math":
            math_text = (
                "📐 *Higher Mathematics Cheatsheet:*\n\n"
                "• Common Indefinite Integrals:\n"
                "  `∫ x^n dx = (x^(n+1))/(n+1) + C`\n"
                "  `∫ (1/x) dx = ln|x| + C`\n"
                "• Table of Derivatives:\n"
                "  `(x^n)' = n * x^(n-1)`\n"
                "  `(ln(x))' = 1/x`"
            )
            bot.send_message(chat_id, math_text, parse_mode="Markdown")
            
        # 13. Physics Formulas Response
        elif call.data == "shpor_phys":
            phys_text = (
                "⚡ *Physics (Electrodynamics):*\n\n"
                "• Ohm's Law for a uniform circuit section:\n"
                "  `I = U / R`\n"
                "• Kirchhoff's Rules:\n"
                "  1. The algebraic sum of currents in any node is zero.\n"
                "  2. The algebraic sum of voltage drops in any closed loop equals the total EMF."
            )
            bot.send_message(chat_id, phys_text, parse_mode="Markdown")
            
        # 14. View Tasks via Inline Button
        elif call.data == "tasks_view":
            user_tasks = db.get_tasks(call.from_user.id)
            if not user_tasks:
                bot.send_message(chat_id, "Your task list is empty.")
            else:
                response = "📋 *Your Tasks:*\n" + "\n".join([f"- {t}" for t in user_tasks])
                bot.send_message(chat_id, response, parse_mode="Markdown")
                
        # 15. Add Task State Transition via Inline Button
        elif call.data == "tasks_add":
            user_states[chat_id] = 'waiting_for_task'
            bot.send_message(chat_id, "⌨️ Type your task/note and send it as a message:")
            
        # Clear Tasks via Inline Button
        elif call.data == "tasks_clear":
            db.clear_tasks(call.from_user.id)
            bot.send_message(chat_id, "🗑️ Task list cleared.")
            
        bot.answer_callback_query(call.id)