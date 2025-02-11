from telethon import TelegramClient, events, Button
import os

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# قاموس لتخزين عدد الإعجابات وعدم الإعجابات لكل رسالة
votes = {}

@client.on(events.NewMessage(pattern=r'^تصويت\s+(.+)$'))
async def my_event_handler(event):
    match = event.pattern_match
    isabh = event.sender_id

    if match and isabh != 1910015590:
        text = match.group(1)  # استخراج النص بعد "تصويت"
        message_id = event.message.id  # تخزين معرف الرسالة لربط التصويت بها
        votes[message_id] = {"like": 0, "dislike": 0}

        buttons = [
            [Button.inline(f"👍 0", f"yes_{message_id}".encode())],
            [Button.inline(f"👎 0", f"no_{message_id}".encode())]
        ]

        await event.respond(f"🗳 {text}", buttons=buttons)

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode()
    if data.startswith("yes_") or data.startswith("no_"):
        message_id = int(data.split("_")[1])  # استخراج معرف الرسالة من البيانات
        if message_id in votes:
            if data.startswith("yes_"):
                votes[message_id]["like"] += 1
            else:
                votes[message_id]["dislike"] += 1

            # تحديث الأزرار
            buttons = [
                [Button.inline(f"👍 {votes[message_id]['like']}", f"yes_{message_id}".encode())],
                [Button.inline(f"👎 {votes[message_id]['dislike']}", f"no_{message_id}".encode())]
            ]
            await event.edit(buttons=buttons)

client.run_until_disconnected()
