from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telethon import TelegramClient, events, Button
import os
# الحصول على متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تهيئة عميل البوتimport smtplib
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# المتغيرات لتخزين البيانات
user_data = {}

@ABH.on(events.NewMessage(pattern='^/start$'))
async def start(event):
    chat_id = event.chat_id
    user_data[chat_id] = {"sender_email": None, "password": None, "receiver_email": None, "text": None, "subject": None}
    await event.reply(
        "أهلاً بك! اختر ما تريد إضافته:",
        buttons=[
            [Button.inline("اضف ايميل", b"email")],
            [Button.inline("اضف باسورد", b"pass")],
            [Button.inline("اضف مستلم", b"to")],
            [Button.inline("اضف كليشة", b"text")],
            [Button.inline("اضف موضوع", b"subject")],
            [Button.inline("إرسال البريد 100 مرة", b"send_email")]
        ]
    )

@ABH.on(events.CallbackQuery)
async def callback(event):
    chat_id = event.chat_id
    data = event.data.decode("utf-8")

    if chat_id not in user_data:
        user_data[chat_id] = {"sender_email": None, "password": None, "receiver_email": None, "text": None, "subject": None}

    if data == "email":
        await event.respond("أدخل البريد المرسل:")
        user_data[chat_id]["awaiting"] = "sender_email"

    elif data == "pass":
        await event.respond("أدخل كلمة المرور:")
        user_data[chat_id]["awaiting"] = "password"

    elif data == "to":
        await event.respond("أدخل البريد المستلم:")
        user_data[chat_id]["awaiting"] = "receiver_email"

    elif data == "text":
        await event.respond("أدخل الكليشة:")
        user_data[chat_id]["awaiting"] = "text"

    elif data == "subject":
        await event.respond("أدخل الموضوع:")
        user_data[chat_id]["awaiting"] = "subject"

    elif data == "send_email":
        await send_email(chat_id, event)

@ABH.on(events.NewMessage)
async def handle_input(event):
    chat_id = event.chat_id
    if chat_id in user_data and "awaiting" in user_data[chat_id]:
        key = user_data[chat_id]["awaiting"]
        user_data[chat_id][key] = event.text
        del user_data[chat_id]["awaiting"]
        await event.respond(f"تم حفظ {key} بنجاح.")

async def send_email(chat_id, event):
    data = user_data.get(chat_id, {})
    sender_email = data.get("sender_email")
    password = data.get("password")
    receiver_email = data.get("receiver_email")
    text = data.get("text")
    subject = data.get("subject")

    # تحقق من جميع القيم
    if not all([sender_email, password, receiver_email, text, subject]):
        await event.respond("يجب ملء جميع البيانات قبل الإرسال.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # إضافة النصوص
    message.attach(MIMEText(text, "plain"))

    # إرسال البريد 100 مرة
    for i in range(100):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Email {i+1} sent successfully!")
        except Exception as e:
            print(f"Failed to send email {i+1}: {e}")
            break

    await event.respond("تم إرسال البريد 100 مرة بنجاح!")

# تشغيل البوت
print("Bot is running...")
ABH.run_until_disconnected()

