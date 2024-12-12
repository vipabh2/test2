import os
import random
import telebot
from telebot import types
bot = telebot.TeleBot("7273443857:AAFt8PtcI_gdYp0QbtcJH1Tu1oFJn9-H0yk")

is_game_started = False
is_word_sent = False
word = ''
points = {}

# دالة لبدء اللعبة
@bot.message_handler(commands=['اسرع'])
def start_game(message):
    global is_game_started, is_word_sent, word
    # أخذ الكلمة التي يجب على اللاعبين كتابتها
    word = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else ''
    
    if word:
        is_game_started = True
        is_word_sent = False
        bot.reply_to(message, f"**اول من يكتب ( {word} ) سيفوز**")
    else:
        bot.reply_to(message, "الرجاء إدخال الكلمة التي يجب كتابتها بعد الأمر.")
        
# دالة للتعامل مع الرسائل المرسلة من المستخدمين
@bot.message_handler(func=lambda message: is_game_started and not is_word_sent)
def handle_winner(message):
    global is_game_started, is_word_sent, word, points
    
    # إذا كانت الرسالة تحتوي على الكلمة المطلوبة
    if word.lower() in message.text.lower():
        is_word_sent = True
        winner_id = message.from_user.id
        
        # إضافة نقاط اللاعب الفائز
        if winner_id not in points:
            points[winner_id] = 0
        points[winner_id] += 1
        
        # الحصول على اسم الفائز
        winner_name = message.from_user.first_name if message.from_user.first_name else "مجهول"
        
        # ترتيب اللاعبين حسب النقاط
        sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
        points_text = '\n'.join([f'{i+1}• {bot.get_chat_member(message.chat.id, participant_id).user.first_name}: {participant_points}' 
                                for i, (participant_id, participant_points) in enumerate(sorted_points)])
        
        # إرسال رسالة الفائز
        bot.send_message(message.chat.id, f"الف مبروووك 🎉 الاعب ( {winner_name} ) فاز! \n اصبحت نقاطه: {points[winner_id]}\nنقاط المشاركين:\n{points_text}")
        is_game_started = False  # إنهاء اللعبة بعد إعلان الفائز


if __name__ == "__main__":
    bot.polling(none_stop=True)
