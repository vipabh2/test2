from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = mention.pattern_match.group(0)
    if not user:
        return
    if custom:
        return await mention.reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await mention.reply(mention, f"⌔︙[{tag}](tg://user?id={user.id})")


client.start()
client.run_until_disconnected()
