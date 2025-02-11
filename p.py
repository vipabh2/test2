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
vote_text = ""

@client.on(events.NewMessage(pattern=r'^تصويت\s+(.+)$'))
async def handler(event):
    global vote_text
    vote_text = event.pattern_match.group(1)
    await event.respond(
        f'{vote_text}',
        buttons=[
            [Button.inline(f'👍 {votes["button1"]}', data='button1')],
            [Button.inline(f'👎 {votes["button2"]}', data='button2')]
        ]
    )

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')

    if data == 'button1':
        votes['button1'] += 1
    elif data == 'button2':
        votes['button2'] += 1

    await event.edit(
        f'{vote_text}',
        buttons=[
            [Button.inline(f'👍 {votes["button1"]}', data='button1')],
            [Button.inline(f'👎 {votes["button2"]}', data='button2')]
        ]
    )

client.run_until_disconnected()
