from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def handle_id_command(mention):
    """كشف ايدي باستخدام الرقم المرسل في الأمر"""
    # استخراج ID المستخدم من الرسالة
    user_id = mention.pattern_match.group(1)
    
    # استرجاع معلومات المستخدم بناءً على ID
    try:
        user = await client.get_entity(user_id)
    except Exception as e:
        await mention.reply(f"لم يتم العثور على مستخدم بهذا الرقم ID: {user_id}")
        return

    # إنشاء الرابط إلى المحادثة الخاصة
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await mention.reply(f"⌔︙[{tag}](tg://user?id={user.id})")

client.start()
client.run_until_disconnected()
