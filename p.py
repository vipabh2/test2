from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(mention):
    """Generates a link to the user's PM based on the ID."""
    user_id = mention.pattern_match.group(1)  # استخراج رقم الـ ID من الرسالة
    try:
        # إرسال رابط الحساب مباشرة باستخدام الـ ID
        await mention.reply(f"⌔︙tg://user?id={user_id}")
    except Exception as e:
        await mention.reply("حدث خطأ أثناء محاولة العثور على المستخدم.")  # في حال حدوث مشكلة

client.start()
client.run_until_disconnected()
