from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonCallback
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('session_name', api_id, api_hash)

@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(event):
    user_id = event.pattern_match.group(1)
    try:
        user = await event.client.get_entity(int(user_id))
    except ValueError:
        return await event.reply("User not found.")
    if not user:
        return await event.reply(f"User not found.")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.reply(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])

@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    user_id = event.pattern_match.group(1)
    user = await event.client.get_entity(int(user_id))
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.edit(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])

ABH.start(bot_token=bot_token)
ABH.run_until_disconnected()
