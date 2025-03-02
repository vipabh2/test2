from telethon import TelegramClient, events
import os
import json

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تشغيل العميل
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(chats="channel_username"))  # استبدل بمعرف القناة
async def mark_as_read(event):
    await ABH.send_read_acknowledge(event.chat_id)  # يحاول يسوي Seen
    print(f"✅ تمت محاولة قراءة رسالة بالقناة: {event.text}")

print("✅ البوت يعمل...")
ABH.run_until_disconnected()
