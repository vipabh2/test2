import os
import telebot
import random

bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)

game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
group_game_status = {}
points = {}
joker = ["🤔", "🙄", "😳", "🥲", "😜"]

# دالة لتنسيق اللوحة
def format_board(game_board, numbers_board):
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board

# متغير لتخزين اللاعبين المحظورين
banned_users = [7465920634, 6048901890]

# التعامل مع الأمر "/محيبس" لبدء اللعبة
@bot.message_handler(commands=['محيبس'])
def start(message):
    if message.from_user.id in banned_users:
        bot.reply_to(message, "عذرا , انت محظور من استخدام البوت.")
        return

    chat_id = message.chat.id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started2': False, 'joker_player': None}

    # بدء اللعبة
    if not group_game_status[chat_id]['is_game_started2']:
        group_game_status[chat_id]['is_game_started2'] = True
        group_game_status[chat_id]['joker_player'] = None
        bot.reply_to(message, f"تم بدء اللعبة! لفتح العضمة ارسل 'طك رقم العضمة' للمشاركة.")

# التعامل مع التحديثات عندما يرسل المستخدم "طك رقم العضمة"
@bot.message_handler(regexp=r'\طك (\d+)')
def handle_strike(message):
    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started2']:
        strike_position = int(message.text.split()[1])
        correct_answer = random.randint(1, 6)  # الإجابة الصحيحة عشوائيًا
        if strike_position == correct_answer:
            game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
            bot.reply_to(message, f"**خسرت!** \n{format_board(game_board, numbers_board)}")
            game_board = [row[:] for row in original_game_board]
            group_game_status[chat_id]['is_game_started2'] = False
            group_game_status[chat_id]['joker_player'] = None
        else:
            game_board[0][strike_position - 1] = '🖐️'
            bot.reply_to(message, f"**العضمة لم تجد المحبس!** \n{format_board(game_board, numbers_board)}")

# التعامل مع كلمة "انا" لتسجيل اللاعب الجوكر
@bot.message_handler(regexp=r'\انا')
def handle_incoming_message(message):
    chat_id = message.chat.id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started2': False, 'joker_player': None}
    if group_game_status[chat_id]['is_game_started2'] and not group_game_status[chat_id]['joker_player']:
        group_game_status[chat_id]['joker_player'] = message.from_user.id
        bot.reply_to(message, f"**تم تسجيلك في المسابقة!** \n{format_board(game_board, numbers_board)}")

# التعامل مع كلمة "جيب" لتخمين رقم العضمة
@bot.message_handler(regexp=r'\جيب (\d+)')
def handle_guess(message):
    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started2'] and message.from_user.id == group_game_status[chat_id]['joker_player']:
        guess = int(message.text.split()[1])
        correct_answer = random.randint(1, 6)  # الإجابة الصحيحة عشوائيًا
        if 1 <= guess <= 6:
            if guess == correct_answer:
                winner_id = message.from_user.id
                if winner_id not in points:
                    points[winner_id] = 0
                points[winner_id] += 1
                sender_first_name = message.from_user.first_name
                sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
                points_text = '\n'.join([f'{i+1}• {sender_first_name}: {participant_points}' for i, (participant_id, participant_points) in enumerate(sorted_points)])
                game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
                bot.send_message(message.chat.id, f'الف مبروووك 🎉 الاعب ( {sender_first_name} ) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}')
                game_board = [row[:] for row in original_game_board]
                bot.send_message(message.chat.id, f'نقاط الاعب : {points[winner_id]}\nنقاط المشاركين:\n{points_text}')
            else:
                game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
                bot.reply_to(message, f"**ضاع البات ماضن بعد تلگونة ☹️\n{format_board(game_board, numbers_board)}**")
                game_board = [row[:] for row in original_game_board]
            group_game_status[chat_id]['is_game_started2'] = False
            group_game_status[chat_id]['joker_player'] = None

# بدء البوت
bot.polling()
