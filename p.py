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

@client.on(events.NewMessage(pattern='/تصويت'))
async def handler(event):
    # إظهار الأزرار مع النص
    await event.respond(
        'اختار واحد من الأزرار:',
        buttons=[
            [Button.inline(f'زر 1 - {votes["button1"]}', data='button1')],
            [Button.inline(f'زر 2 - {votes["button2"]}', data='button2')]
        ]
    )

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')

    if data == 'button1':
        votes['button1'] += 1
    elif data == 'button2':
        votes['button2'] += 1

    # إعادة إرسال الأزرار مع تحديث الأعداد
    await event.edit(
        f'اختار واحد من الأزرار:',
        buttons=[
            [Button.inline(f'زر 1 - {votes["button1"]}', data='button1')],
            [Button.inline(f'زر 2 - {votes["button2"]}', data='button2')]
        ]
    )




client.run_until_disconnected()
