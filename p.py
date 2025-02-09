from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('session_name', api_id, api_hash)

# حالة المستخدمين
user_states = {}

@ABH.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    user_states[user_id] = {'step': 'get_subject'}
    await event.respond("مرحبًا! أرسل موضوع الرسالة.")

@ABH.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id

    if user_id not in user_states:
        return

    state = user_states[user_id]
    step = state.get('step')

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
        # إرسال الفيديو مع الرسالة
        await event.respond(
            "أرسل كلمة المرور (كلمة مرور التطبيق كما في الفيديو)",
            file="https://t.me/recoursec/2"
        )

    elif step == 'get_password':
        state['password'] = event.text
        subject = state.get('subject')
        body = state.get('body')
        recipient = state.get('recipient')
        sender_email = state.get('sender_email')
        password = state.get('password')

        # هنا يمكنك إضافة الكود لإرسال البريد الإلكتروني
        await event.respond("تم استلام جميع المعلومات بنجاح!")

        # مسح حالة المستخدم بعد الانتهاء
        del user_states[user_id]

ABH.start(bot_token=bot_token)
ABH.run_until_disconnected()
