import os
import telebot
from telebot import types
import random

bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)



group_game_status = {}

banned_users = []

def format_board(game_board, numbers_board):
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board

# دالة لإعادة ضبط اللعبة
def reset_game(chat_id):
    group_game_status[chat_id] = {
        "is_game_started": False,
        "joker_player": None,
        "correct_answer": None,
        "game_board": [["👊"] * 6],
    }

# بدء اللعبة عند تلقي كلمة "محيبس"
@bot.message_handler(func=lambda message: message.text == 'محيبس')
def start_game_handler(message):
    chat_id = message.chat.id

    # إنشاء حالة اللعبة إذا لم تكن موجودة
    if chat_id not in group_game_status:
        reset_game(chat_id)

    # تحقق إذا كانت اللعبة بدأت بالفعل
    if group_game_status[chat_id]["is_game_started"]:
        bot.reply_to(message, "اللعبة جارية بالفعل!")
        return

    # إعداد اللعبة
    group_game_status[chat_id]["is_game_started"] = True
    group_game_status[chat_id]["correct_answer"] = random.randint(1, 6)

    # إعداد لوحة المفاتيح التفاعلية
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ابدأ اللعبة", callback_data="start_game"))

    username = message.from_user.username or "unknown"
    bot.send_video(
        chat_id,
        "https://your_video_link_here.mp4",  # استبدل برابط فيديو مباشر
        caption=f"أهلاً [{message.from_user.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        parse_mode="Markdown",
        reply_markup=markup
    )

# عند الضغط على زر "ابدأ اللعبة"
@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def handle_start_game(call):
    chat_id = call.message.chat.id

    if chat_id in group_game_status and group_game_status[chat_id]["is_game_started"]:
        bot.send_message(chat_id, f"تم اختيار الرقم السري! اللعبة جاهزة. لفتح العضمة أرسل 'طك <رقم>'.")
    else:
        bot.send_message(chat_id, "يرجى إعادة بدء اللعبة عن طريق إرسال 'محيبس'.")

# التعامل مع الأمر "طك <رقم>"
@bot.message_handler(regexp=r'\طك (\d+)')
def handle_strike(message):
    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]["is_game_started"]:
        try:
            strike_position = int(message.text.split()[1])
            correct_answer = group_game_status[chat_id]["correct_answer"]
            game_board = group_game_status[chat_id]["game_board"]

            if strike_position == correct_answer:
                game_board[0][strike_position - 1] = "💍"
                bot.send_message(chat_id, f"🎉 **خسرت اللعبة!**\n{format_board(game_board, [['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']])}")
                reset_game(chat_id)
            else:
                game_board[0][strike_position - 1] = "🖐️"
                bot.send_message(chat_id, f"❌ **خاطئ! حاول مرة أخرى.**\n{format_board(game_board, [['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']])}")
        except (IndexError, ValueError):
            bot.reply_to(message, "❗ يرجى إدخال رقم صحيح بين 1 و 6.")
    else:
        bot.reply_to(message, "❗ اللعبة لم تبدأ بعد. أرسل 'محيبس' لبدء اللعبة.")

# التعامل مع الأمر "جيب <رقم>"
@bot.message_handler(regexp=r'\جيب (\d+)')
def handle_guess(message):
    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]["is_game_started"]:
        try:
            guess = int(message.text.split()[1])
            correct_answer = group_game_status[chat_id]["correct_answer"]

            if guess == correct_answer:
                bot.send_message(chat_id, f"🎉 **مبروك! وجدت المحبس!** 💍")
                reset_game(chat_id)
            else:
                bot.reply_to(message, "❌ الرقم غير صحيح. حاول مرة أخرى.")
        except ValueError:
            bot.reply_to(message, "❗ يرجى إدخال رقم صحيح.")
    else:
        bot.reply_to(message, "❗ اللعبة لم تبدأ بعد. أرسل 'محيبس' لبدء اللعبة.")

# تشغيل البوت
bot.polling()
