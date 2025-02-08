from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
        # user, custom = await get_user_from_event(mention)
    # if not user:
    #     return
    # if custom:
        # return
    user = mention.pattern_match.group(0)
    await mention.reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await mention.reply(mention, f"⌔︙[{tag}](tg://user?id={user.id})")


client.start()
client.run_until_disconnected()
