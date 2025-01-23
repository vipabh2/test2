from telethon import TelegramClient, events, Button
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

default_smtp_server = "smtp.gmail.com"
default_smtp_port = 465

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# State management dictionary
user_states = {}

def create_email_message(subject, body, recipient):
    return f"Subject: {subject}\nTo: {recipient}\n\n{body}"

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.inline("إنشاء رسالة", b"create_message")],
    ]
    await event.respond(
        "أهلاً بك في بوت إنشاء الرسائل! اختر أحد الخيارات أدناه:",
        buttons=buttons
    )

@client.on(events.CallbackQuery(data=b"create_message"))
async def create_message(event):
    user_states[event.sender_id] = {'step': 'get_subject'}
    await event.respond("أرسل الموضوع (Subject) للرسالة:")

@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    if user_id not in user_states:
        return

    state = user_states[user_id]
    step = state['step']

    if step == 'get_subject':
        state['subject'] = event.text
        state['step'] = 'get_body'
        await event.respond("أرسل نص الكليشة (Body) للرسالة:")
    elif step == 'get_body':
        state['body'] = event.text
        state['step'] = 'get_recipient'
        await event.respond("أرسل الإيميل المستلم (Recipient Email):")
    elif step == 'get_recipient':
        state['recipient'] = event.text
        state['step'] = 'get_email'
        await event.respond("أرسل بريدك الإلكتروني (Sender Email):")
    elif step == 'get_email':
        state['sender_email'] = event.text
        state['step'] = 'get_password'
        await event.respond("أرسل كلمة المرور (Email Password):")
    elif step == 'get_password':
        state['password'] = event.text
        subject = state['subject']
        body = state['body']
        recipient = state['recipient']
        sender_email = state['sender_email']
        password = state['password']

        email_message = create_email_message(subject, body, recipient)
        buttons = [
            [Button.inline("إرسال الرسالة", b"send_email")]
        ]
        await event.respond(
            f"تم إنشاء الرسالة التالية:\n\n{email_message}\n\nاضغط على الزر أدناه لإرسالها:",
            buttons=buttons
        )
        state['step'] = 'confirm_send'

@client.on(events.CallbackQuery(data=b"send_email"))
async def send_email(event):
    user_id = event.sender_id
    if user_id not in user_states or user_states[user_id]['step'] != 'confirm_send':
        return

    state = user_states[user_id]
    subject = state['subject']
    body = state['body']
    recipient = state['recipient']
    sender_email = state['sender_email']
    password = state['password']

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL(default_smtp_server, default_smtp_port) as server:
            server.login(sender_email, password)
            for i in range(100):
                server.sendmail(sender_email, recipient, message.as_string())
                print(f"Email {i + 1} sent successfully.")

        await event.respond("تم إرسال الرسالة 100 مرة بنجاح!")
    except smtplib.SMTPException as e:
        if "Connection unexpectedly closed" in str(e):
            await event.respond("فشل الإرسال بسبب انقطاع الاتصال بالسيرفر. تأكد من بيانات الاتصال وأعد المحاولة.")
        else:
            await event.respond(f"حدث خطأ أثناء الإرسال: {e}")
    except Exception as e:
        await event.respond(f"حدث خطأ غير متوقع: {e}")

client.run_until_disconnected()
