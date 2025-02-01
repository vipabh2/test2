from telethon import TelegramClient, events
import os, random 

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='/start'))
async def reply_abh(event):
    iu = random.choice(["ch1", "ch2"])  
    if iu == "ch1":  
        rl = random.randint(1222, 1223)
        url = f"https://t.me/VIPABH/{rl}"
    else:  
        rl = random.randint(242, 255)
        url = f"https://t.me/iuABH/{rl}"  

    caption = "ابن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
    await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)   

ABH.run_until_disconnected()
