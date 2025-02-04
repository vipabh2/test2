from telethon import TelegramClient, events, Button
import os, random

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='/start'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        rl = random.randint(1222, 1241)
        url = f"https://t.me/VIPABH/{rl}"
        caption = "ابن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
        button = [Button.url("الking", "https://t.me/K_4x1")]
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id, buttons=button)
    else:
        return

print("Bot is running...")
ABH.run_until_disconnected()
