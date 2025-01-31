from telethon import TelegramClient, events
import os, random 

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
c = [
    "ههههههه",
    "راويني السنون الصفر",
    "اضحك شبيك شايل الدنية علئ اجتافك",
    "صح سخيفة بس هههه حلوه",
    "انت طلبت الامر ليش ما ضحكت",
    "😂",
    "يسعدلي مسائك😀"
]
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.NewMessage(pattern='/start$'))
async def start(event):
    global c
    rl = random.randint(2, 273)
    url = f"https://t.me/IUABH/{rl}"
    cap = random.choice(c)
    await ABH.send_file(event.chat_id, url, caption=f"{cap}")

ABH.run_until_disconnected()
