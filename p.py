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

def create_email_message(subject, body, recipient):
    return f"Subject: {subject}\nTo: {recipient}\n\n{body}"

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    user_states[user_id] = {}
    buttons = [
        [Button.inline("إنشاء رسالة", b"create_message")],
        [Button.inline("الحساب الاول", b"a1")],
        [Button.inline("الحساب الثاني", b"a2")],
        [Button.inline("الحساب الثالث", b"a3")]
    ]
    await event.respond(
        "اهلا اخي حياك الله, البوت مجاني حاليا يرفع بلاغات بصوره امنة وحقيقية\n المطور @K_4X1",
        buttons=buttons
    )

@client.on(events.CallbackQuery(data=b"create_message"))
async def create_message(event):
    user_states[event.sender_id] = {'step': 'get_subject'}
    await event.edit("أرسل الموضوع (الكليشة القصيرة)")

@client.on(events.CallbackQuery(data=b"a1"))
async def account_a1(event):
    user_states[event.sender_id] = {'account': 'a1', 'step': 'get_subject'}
    await event.edit("أرسل الموضوع (الكليشة القصيرة) للحساب الأول")

@client.on(events.CallbackQuery(data=b"a2"))
async def account_a2(event):
    user_states[event.sender_id] = {'account': 'a2', 'step': 'get_subject'}
    await event.edit("أرسل الموضوع (الكليشة القصيرة) للحساب الثاني")

@client.on(events.CallbackQuery(data=b"a3"))
async def account_a3(event):
    user_states[event.sender_id] = {'account': 'a3', 'step': 'get_subject'}
    await event.edit("أرسل الموضوع (الكليشة القصيرة) للحساب الثالث")

@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    if user_id not in user_states:
        return

    state = user_states[user_id]
    step = state.get('step')
    account = state.get('account', 'default')
    
    if step == 'get_subject':
        state[f'subject_{account}'] = event.text
        state['step'] = 'get_body'
        await event.respond("أرسل نص الكليشة (الكليشة الكبيرة)")
    elif step == 'get_body':
        state[f'body_{account}'] = event.text
        state['step'] = 'get_recipient'
        await event.respond("أرسل الإيميل المستلم (`abuse@telegram.org`)")
    elif step == 'get_recipient':
        state[f'recipient_{account}'] = event.text
        state['step'] = 'get_email'
        await event.respond("أرسل بريدك الإلكتروني (الايميل الذي تريد منه الارسال)")
    elif step == 'get_email':
        state[f'sender_email_{account}'] = event.text
        state['step'] = 'get_password'
        await event.respond("أرسل كلمة المرور (كلمة مرور التطبيق كما في الفيديو)")
    elif step == 'get_password':
        state[f'password_{account}'] = event.text
        email_message = create_email_message(state[f'subject_{account}'], state[f'body_{account}'], state[f'recipient_{account}'])
        buttons = [[Button.inline("إرسال الرسالة", b"send_email")]]
        await event.respond(f"تم إنشاء الكليشة التالية:\n\n{email_message}\n\nاضغط على الزر أدناه لإرسالها", buttons=buttons)
        state['step'] = 'confirm_send'

@client.on(events.CallbackQuery(data=b"send_email"))
async def send_email(event):
    user_id = event.sender_id
    if user_id not in user_states or user_states[user_id].get('step') != 'confirm_send':
        await event.edit("هناك نقص في المعلومات. حاول مرة أخرى باستخدام /start")
        return

    state = user_states[user_id]
    account = state.get('account', 'default')
    
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = state[f'subject_{account}']
        message["From"] = state[f'sender_email_{account}']
        message["To"] = state[f'recipient_{account}']
        message.attach(MIMEText(state[f'body_{account}'], "plain"))

        with smtplib.SMTP_SSL(default_smtp_server, default_smtp_port) as server:
            server.login(state[f'sender_email_{account}'], state[f'password_{account}'])
            for i in range(10):
                server.sendmail(state[f'sender_email_{account}'], state[f'recipient_{account}'], message.as_string())
                await event.respond(f"تم الإرسال {i+1} بنجاح")
                await asyncio.sleep(1)
    except smtplib.SMTPException as e:
        await event.respond(f"حدث خطأ أثناء الإرسال: {e}")
    except Exception as e:
        await event.respond(f"حدث خطأ غير متوقع: {e}")

client.run_until_disconnected()
