import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telethon import TelegramClient, events
import os

# الحصول على متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# المتغيرات العامة
sender_email = None
receiver_email = "abuse@telegram.org"
subject = None
email_text = None

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    global password
    password = "fzuf heoh foqw tdge"
    await event.reply(
        "مرحبًا! لإرسال إيميل، قم بإدخال البيانات كما يلي:\n\n" +
        "/email <البريد المرسل>\n" +
        "/password <كلمة المرور>\n" +
        "/subject <الموضوع>\n" +
        "/text <نص الرسالة>\n\n" +
        "بعد إدخال جميع البيانات، أرسل /send لبدء إرسال الإيميل."
    )

@bot.on(events.NewMessage(pattern='/email (.+)'))
async def set_email(event):
    global sender_email
    sender_email = event.pattern_match.group(1)
    await event.reply(f"تم حفظ البريد المرسل: {sender_email}")

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
    if not all([sender_email, password, subject, email_text]):
        await event.reply("الرجاء إدخال جميع البيانات المطلوبة قبل الإرسال.")
        return

    # إعداد الرسالة
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(email_text, "plain"))
    message.attach(MIMEText(f"<html><body><p>{email_text}</p></body></html>", "html"))

    try:
        for i in range(100):
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            await event.reply(f"تم إرسال الإيميل {i+1} بنجاح!")
    except smtplib.SMTPException as e:
        if "Daily user sending limit exceeded" in str(e):
            await event.reply("تم تجاوز الحد اليومي لإرسال الرسائل. الرجاء المحاولة غدًا.")
        else:
            await event.reply(f"فشل إرسال الإيميل: {e}")
    except Exception as e:
        await event.reply(f"حدث خطأ غير متوقع أثناء الإرسال: {e}")

print("Bot is running...")
bot.run_until_disconnected()
