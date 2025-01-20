import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telethon import TelegramClient, events
import os
# الحصول على متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تهيئة عميل البوتimport smtplib
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

sender_email = None
receiver_email = None
password = None
subject = None
email_text = None

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("مرحبًا! لإرسال إيميل، قم بإدخال البيانات كما يلي:\n\n" +
                      "/email <البريد المرسل>\n" +
                      "/password <كلمة مرور البريد>\n" +
                      "/to <البريد المستلم>\n" +
                      "/subject <الموضوع>\n" +
                      "/text <نص الرسالة>\n\n" +
                      "بعد إدخال جميع البيانات، أرسل /send لبدء إرسال الإيميل.")

@bot.on(events.NewMessage(pattern='/email (.+)'))
async def set_email(event):
    global sender_email
    sender_email = event.pattern_match.group(1)
    await event.reply(f"تم حفظ البريد المرسل: {sender_email}")

@bot.on(events.NewMessage(pattern='/password (.+)'))
async def set_password(event):
    global password
    password = event.pattern_match.group(1)
    await event.reply("تم حفظ كلمة المرور بنجاح.")

@bot.on(events.NewMessage(pattern='/to (.+)'))
async def set_receiver(event):
    global receiver_email
    receiver_email = event.pattern_match.group(1)
    await event.reply(f"تم حفظ البريد المستلم: {receiver_email}")

@bot.on(events.NewMessage(pattern='/subject (.+)'))
async def set_subject(event):
    global subject
    subject = event.pattern_match.group(1)
    await event.reply(f"تم حفظ الموضوع: {subject}")

@bot.on(events.NewMessage(pattern='/text (.+)'))
async def set_text(event):
    global email_text
    email_text = event.pattern_match.group(1)
    await event.reply("تم حفظ نص الرسالة.")

@bot.on(events.NewMessage(pattern='/send'))
async def send_email(event):
    if not all([sender_email, password, receiver_email, subject, email_text]):
        await event.reply("الرجاء إدخال جميع البيانات المطلوبة قبل الإرسال.")
        return

    # إعداد الرسالة
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(email_text, "plain"))

    try:
        # إرسال الإيميل باستخدام SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        await event.reply("تم إرسال الإيميل بنجاح!")
    except Exception as e:
        await event.reply(f"فشل إرسال الإيميل: {e}")

print("Bot is running...")
bot.run_until_disconnected()
