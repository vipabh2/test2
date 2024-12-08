
import os
import random
import telebot
from telebot import types 

bot = telebot.TeleBot("7273443857:AAFt8PtcI_gdYp0QbtcJH1Tu1oFJn9-H0yk")

game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
group_game_status = {}
points = {}
joker = ["🤔", "🙄", "😳", "🥲", "😜"]
correct_answer = None  
banned_users = []  

def format_board(game_board, numbers_board):
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board

def reset_game(chat_id):
    global game_board, correct_answer, group_game_status, correct_answer 
    game_board = [row[:] for row in original_game_board]
    correct_answer = None
    group_game_status[chat_id]['is_game_started2'] = False
    group_game_status[chat_id]['joker_player'] = None

@bot.message_handler(func=lambda message: message.text == 'محيبس')
def strt(message):
    global correct_answer 
    markup = types.InlineKeyboardMarkup() 
    markup.add(types.InlineKeyboardButton("ابدأ اللعبة", callback_data="start_game"))

    username = message.from_user.username or "unknown"
    bot.send_video(
        message.chat.id,
        "t.me/VIPABH/1210",  
        caption=f"أهلاً [{message.from_user.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        parse_mode="Markdown",
        reply_markup=markup
    ) 
 
    chat_id = message.chat.id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started2': False, 'joker_player': None}

    if not group_game_status[chat_id]['is_game_started2']:
        group_game_status[chat_id]['is_game_started2'] = True
        group_game_status[chat_id]['joker_player'] = None
        correct_answer = random.randint(1, 6)  
        bot.reply_to(message, f"تم بدء اللعبة! لفتح العضمة ارسل 'طك رقم العضمة' للمشاركة.")



@bot.message_handler(regexp=r'\طك (\d+)')
def handle_strike(message):
    global correct_answer, game_board  # تأكد من أنك تستخدم المتغيرات بشكل صحيح

    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started2']:
        try:
            strike_position = int(message.text.split()[1])
            if strike_position == correct_answer:
                game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
                winner_id = message.from_user.id
                points[winner_id] = points.get(winner_id, 0) + 1  # إضافة نقطة للفائز
                bot.reply_to(message, f"**مبروك! لقد فزت!** 🎉 \n{format_board(game_board, numbers_board)}")
                reset_game(chat_id)  # إعادة تعيين اللعبة
            else:
                game_board[0][strike_position - 1] = '🖐️'
                bot.reply_to(message, f"**العضمة لم تجد المحبس!** \n{format_board(game_board, numbers_board)}")
        except (IndexError, ValueError):
            bot.reply_to(message, "يرجى إدخال رقم صحيح بين 1 و 6.")

@bot.message_handler(regexp=r'\انا')
def handle_incoming_message(message):
    chat_id = message.chat.id
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'is_game_started2': False, 'joker_player': None}
    if group_game_status[chat_id]['is_game_started2'] and not group_game_status[chat_id]['joker_player']:
        group_game_status[chat_id]['joker_player'] = message.from_user.id
        bot.reply_to(message, f"**تم تسجيلك في المسابقة!** \n{format_board(game_board, numbers_board)}")

@bot.message_handler(regexp=r'\جيب (\d+)')
def handle_guess(message):
    global group_game_status, correct_answer, game_board, points

    chat_id = message.chat.id
    if chat_id in group_game_status and group_game_status[chat_id]['is_game_started2'] and message.from_user.id == group_game_status[chat_id]['joker_player']:
        try:
            guess = int(message.text.split()[1])
            if 1 <= guess <= 6:
                if guess == correct_answer:
                    winner_id = message.from_user.id
                    points[winner_id] = points.get(winner_id, 0) + 1
                    sender_first_name = message.from_user.first_name
                    game_board = [["💍" if i == correct_answer - 1 else "🖐️" for i in range(6)]]
                    bot.send_message(chat_id, f'الف مبروووك 🎉 الاعب ( {sender_first_name} ) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}')
                    reset_game(chat_id)
                else:
                    bot.reply_to(message, f"**المحبس غير موجود هنا!** \n{format_board(game_board, numbers_board)}")
        except (IndexError, ValueError):
            bot.reply_to(message, "يرجى إدخال رقم صحيح بين 1 و 6.")




bot.polling()

