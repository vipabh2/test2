from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

admins = [
    191001559,
    7176263278,
    6783332896,
    1494932118,
    201728276,
    1688194818,
    5399306464,
    6498922948,
    1446637898
]

@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group:  # تأكد من أن الحدث في مجموعة
        # التحقق إذا كانت الرسالة تحتوي على ملف أو رابط
        if event.media or ('http://' in event.message.message or 'https://' in event.message.message):
            # إذا كانت تحتوي على ملف أو رابط
            await event.reply("تم تعديل الرسالة")
        else:
            # إذا كانت الرسالة لا تحتوي على ملف أو رابط
            await event.reply("تم تعديل الرسالة")
    else:
        return

ABH.run_until_disconnected()
