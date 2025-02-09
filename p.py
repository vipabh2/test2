from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonCallback
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('session_name', api_id, api_hash)

@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(event):
    global user
    user_id = event.pattern_match.group(1)
    if not user_id:
        await event.reply("استخدم الامر ك `كشف ايدي 1910015590`")
    user = await event.client.get_entity(int(user_id))
    if not user:
        return await event.reply(f"لا يوجد حساب بالايدي هذا...")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.reply(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])

@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await event.edit(f"⌔︙(tg://user?id={user.id})")

ABH.start(bot_token=bot_token)
ABH.run_until_disconnected()
