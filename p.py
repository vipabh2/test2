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

def show_account_data(user_id, account):
    state = user_states.get(user_id, {})
    if all(key in state for key in [f'subject_{account}', f'body_{account}', f'recipient_{account}', f'sender_email_{account}', f'password_{account}']):
        email_message = create_email_message(state[f'subject_{account}'], state[f'body_{account}'], state[f'recipient_{account}'])
        return f"البيانات المخزنة للحساب {account}:\n\n{email_message}\n\nاضغط إرسال لإعادة الإرسال", [[Button.inline("إرسال الرسالة", b"send_email")]]
    return f"أرسل الموضوع (الكليشة القصيرة) للحساب {account}", []

@client.on(events.CallbackQuery(pattern=b"a[1-3]"))
async def account_handler(event):
    account = event.data.decode()
    msg, buttons = show_account_data(event.sender_id, account)
    await event.edit(msg, buttons=buttons if buttons else None)

@client.on(events.CallbackQuery(data=b"create_message"))
async def create_message(event):
    user_states[event.sender_id] = {'step': 'get_subject'}
    await event.edit("أرسل الموضوع (الكليشة القصيرة)")

@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    state = user_states.get(user_id, {})
    step = state.get('step')
    account = state.get('account', 'default')
    
    steps = {
        'get_subject': ('subject', "أرسل نص الكليشة (الكليشة الكبيرة)"),
        'get_body': ('body', "أرسل الإيميل المستلم (`abuse@telegram.org`)", 'get_recipient'),
        'get_recipient': ('recipient', "أرسل بريدك الإلكتروني (الايميل الذي تريد منه الارسال)", 'get_email'),
        'get_email': ('sender_email', "أرسل كلمة المرور (كلمة مرور التطبيق كما في الفيديو)", 'get_password')
    }

    if step in steps:
        key, response, next_step = (*steps[step], None) if len(steps[step]) == 2 else steps[step]
        state[f'{key}_{account}'] = event.text
        state['step'] = next_step or f'get_{key}'
        await event.respond(response)
    elif step == 'get_password':
        state[f'password_{account}'] = event.text
        email_message = create_email_message(state[f'subject_{account}'], state[f'body_{account}'], state[f'recipient_{account}'])
        await event.respond(f"تم إنشاء الكليشة التالية:\n\n{email_message}\n\nاضغط على الزر أدناه لإرسالها", buttons=[[Button.inline("إرسال الرسالة", b"send_email")]])
        state['step'] = 'confirm_send'

@client.on(events.CallbackQuery(data=b"send_email"))
async def send_email(event):
    user_id = event.sender_id
    state = user_states.get(user_id, {})
    account = state.get('account', 'default')
    
    if state.get('step') != 'confirm_send':
        await event.edit("هناك نقص في المعلومات. حاول مرة أخرى باستخدام /start")
        return
    
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
