import telebot 

bot = telebot.TeleBot("8155824086:AAEchPPJYWsBG1yESto-dauVkuWklAG4OGk")

username = message.from_user.username if message.from_user.username else "لا يوجد اسم مستخدم"

bot.send_message(call.message.chat.id, f'عزيزي  [{call.from_user.first_name}](https://t.me/@{username}) اختر أي رقم من 1 إلى 10 🌚',  parse_mode="Markdown")
