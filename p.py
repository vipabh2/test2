from telethon import TelegramClient, events
from telethon.tl.custom import Button
import asyncio
import os

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# تخزين عدد الضغطات لكل زر
votes = {'button1': 0, 'button2': 0}

# تخزين معرّفات المستخدمين الذين قاموا بالتصويت
voted_users = set()

@client.on(events.NewMessage(pattern=r'^تصويت\s+(.+)$'))
async def handler(event):
    global vote_text
    isabh = event.sender_id
    txt = event.pattern_match
    if txt and isabh != 1910015590:  # تأكد من أنه ليس البوت الذي أرسل الرسالة
        vote_text = txt.group(1)
    await event.respond(
        f'{vote_text}\n`التصويت اما👍 او 👎 لمره واحده`',  # توضيح بأن التصويت مرة واحدة
        buttons=[
            [Button.inline(f'👍 {votes["button1"]}', data='button1')],
            [Button.inline(f'👎 {votes["button2"]}', data='button2')]
        ]
    )

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')
    user_id = event.sender_id  # الحصول على معرّف المستخدم

    # التحقق إذا كان المستخدم قد صوت بالفعل
    if user_id in voted_users:
        await event.answer("❌ لقد قمت بالتصويت بالفعل!", alert=True)
        return

    if data == 'button1':
        votes['button1'] += 1
    elif data == 'button2':
        votes['button2'] += 1

    # إضافة المستخدم إلى قائمة الذين قاموا بالتصويت
    voted_users.add(user_id)

    await event.edit(
        f'{vote_text}\n`التصويت اما👍 او 👎 لمره واحده`',  # نفس الرسالة مع التحديثات
        buttons=[
            [Button.inline(f'👍 {votes["button1"]}', data='button1')],
            [Button.inline(f'👎 {votes["button2"]}', data='button2')]
        ]
    )

client.run_until_disconnected()
