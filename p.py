from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = mention.sender  # نستخدم sender للوصول إلى المستخدم الذي أرسل الرسالة

    if not user:
        return  # إذا لم يتم العثور على مستخدم، نغادر الدالة

    # نص مخصص يمكن أن يتم استخراج بياناته
    custom = mention.text.split(' ', 1)[1] if len(mention.text.split(' ', 1)) > 1 else None
    
    # إذا كان هناك نص مخصص
    if custom:
        await mention.reply(f"[{custom}](tg://user?id={user.id})")
    else:
        # إذا لم يكن هناك نص مخصص، نعرض اسم المستخدم أو الاسم الأول
        tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
        await mention.reply(f"⌔︙[{tag}](tg://user?id={user.id})")

client.start()
client.run_until_disconnected()
