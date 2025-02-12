from telethon import TelegramClient, events, Button
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
banned_words = [
    "تجربة"
]
smoth_marks = [
    "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"
]
@ABH.on(events.NewMessage)
async def check_banned_words(event):
    if any(word in event.raw_text for word in banned_words and smoth_marks in event.raw_text):
        await event.reply("تم حظرك من استخدام البوت")
        await event.delete()

ABH.run_until_disconnected() 
