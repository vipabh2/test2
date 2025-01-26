from telethon import TelegramClient, events, Button
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, asyncio, smtplib

default_smtp_server = "smtp.gmail.com"
default_smtp_port = 465

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

user_states = {}
isInfo = None

def create_email_message(subject, body, recipient):
    return f"Subject: {subject}\nTo: {recipient}\n\n{body}"

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    global isInfo
    isInfo = None
    buttons = [
        [Button.inline("إنشاء رسالة", b"create_message")],
    ]
    await event.respond(
        "اهلا اخي حياك الله , البوت مجاني حاليا يرفع بلاغات بصوره امنة وحقيقية \n المطور @K_4X1",
        buttons=buttons
    )
@client.on(events.CallbackQuery(data=b"create_message"))
async def create_message(event):
    user_states[event.sender_id] = {'step': 'get_subject'}
    await event.respond("أرسل الموضوع (الكليشة القصيرة)")

@client.on(events.NewMessage)
async def handle_message(event):
    global isInfo
    user_id = event.sender_id
    if user_id not in user_states:
        return

    state = user_states[user_id]
    step = state['step']

    if step == 'get_subject':
        state['subject'] = event.text
        state['step'] = 'get_body'
        await event.respond("أرسل نص الكليشة (الكليشة الكبيرة)")
    elif step == 'get_body':
        state['body'] = event.text
        state['step'] = 'get_recipient'
        await event.respond("أرسل الإيميل المستلم (`abuse@telegram.org`)")
    elif step == 'get_recipient':
        state['recipient'] = event.text
        state['step'] = 'get_email'
        await event.respond("أرسل بريدك الإلكتروني (الايميل الذي تريد منه الارسال)")
    elif step == 'get_email':
        state['sender_email'] = event.text
        state['step'] = 'get_password'
        await event.respond("أرسل كلمة المرور (كلمة مرور التطبيق كما في الفديو)")
        state['sender_email'] = event.text
        state['step'] = 'get_password'
        await event.respond("أرسل كلمة المرور (كلمة مرور التطبيق كما في الفديو)")
    elif step == 'get_password':
        state['password'] = event.text
        subject = state['subject']
        body = state['body']
        recipient = state['recipient']
        sender_email = state['sender_email']
        password = state['password']
        if not subject or not body or not recipient or not sender_email or not password:
            await event.respond("حدث خطأ أثناء جمع البيانات. يرجى المحاولة مرة أخرى.")
            isInfo = False
        else:
            isInfo = True
        email_message = create_email_message(subject, body, recipient)
        buttons = [
            [Button.inline("إرسال الرسالة", b"send_email")]
        ]
        await event.respond(
            f"تم إنشاء الكليشة التالية:\n\n{email_message}\n\nاضغط على الزر أدناه لإرسالها",
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
                await event.edit(f"تم الإرسال {i+1} بنجاح")
                await asyncio.sleep(1)
    except smtplib.SMTPException as e:
        print(f"SMTPException: {e}")
        if "Connection unexpectedly closed" in str(e):
            await event.respond("فشل الإرسال بسبب انقطاع الاتصال بالسيرفر. تأكد من بيانات الاتصال وأعد المحاولة.")
        else:
            await event.respond(f"حدث خطأ أثناء الإرسال: {e}")
    except Exception as e:
        print(f"Exception: {e}")
        await event.respond(f"حدث خطأ غير متوقع: {e}")

    try:
        await event.answer()
    except Exception as query_error:
        print(f"Query Error: {query_error}")
        
@client.on(events.NewMessage(pattern='/send'))
async def send(event):
    global isInfo
    if isInfo == False:
        await event.respond("احدا او كل المعلومات فيها نقص. \n حاول مره اخرئ مع /start")
    elif isInfo == True:
        await event.respond("تم الارسال بنجاح")
        send_email(event)
client.run_until_disconnected()
