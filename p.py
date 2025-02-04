from telethon import TelegramClient, events, Button
import os, time, random
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.NewMessage(pattern='حجرة'))
async def rp(event):
    sender = event.sender_id
    name = event.sender_name
    Button = Button.inline("العب", b"join")
    await event.reply(f"عزيزي {name} تم تسجيلك في اللعبة \n انتظر الاعب الاخر",
                      Button=Button)
    
print("Bot is running...")
ABH.run_until_disconnected()
