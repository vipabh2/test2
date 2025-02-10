import os
from telethon import TelegramClient, events

# الحصول على المتغيرات من البيئة
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء عميل Telethon
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.ChatAction)
async def detect_restriction(event):
    """
    يراقب البوت أي عملية تقييد تحدث في المجموعة، 
    ويرسل إشعارًا فقط دون أي إجراء آخر.
    """
    try:
        if event.user_restricted:
            user = await event.get_user()
            await event.reply(f"🚫 {user.first_name} تم تقييده في المجموعة.")
    except Exception as e:
        print(f"خطأ في معالجة الحدث: {e}")

client.run_until_disconnected()
