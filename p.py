import datetime
from telethon import events, TelegramClient
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='^رمضان$'))
async def cunt(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 3, 1)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^رجب$'))
async def cunt(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 12, 21)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^شعبان$'))
async def cunt(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2026, 2, 2)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^رمضان$'))
async def cunt(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 3, 1)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^محرم$'))
async def cunt(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 6, 26)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
        
print("Bot is running...")
ABH.run_until_disconnected()
