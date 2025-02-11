from telethon import TelegramClient, events, Button
import os

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@client.on(events.NewMessage(pattern=r'^تصويت\s+(.+)$'))
async def my_event_handler(event):
    match = event.pattern_match
    isabh = event.sender_id
    if match and isabh != 1910015590:
        like = 0
        dislike = 0
        Button = [
            [Button.inline(f"👍{like}", b"yes")],
            [Button.inline(f"👎{dislike}", b"no")]
        ]
        await event.respond(
            f"{match}",
            Buttons=Button
        )
@client.on(events.CallbackQuery(data=b"yes"))
async def yes(event):
    global like
    like += 1
    await event.edit(f"👍{like}")
@client.on(events.CallbackQuery(data=b"no"))
async def no(event):
    global dislike
    dislike += 1
    await event.edit(f"👎{dislike}")

client.run_until_disconnected()
