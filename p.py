from telethon import events, TelegramClient, Button
import datetime
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='^/dates$'))
async def cunt(event):
    btton = [[Button.inline("رجب", b"r"), Button.inline("شعبان", b"sh"), Button.inline("رمضان", b"rm"), Button.inline("محرم", b"m")]]
    await event.reply("اختر الشهر المناسب 👇", buttons=btton)
@ABH.on(events.CallbackQuery(data=b"r"))
async def handle_r(event):
    await event.answer()
    await cunt_r(event) 
@ABH.on(events.CallbackQuery(data=b"sh"))
async def handle_r(event):
    await event.answer()
    await cunt_sh(event) 
@ABH.on(events.CallbackQuery(data=b"rm"))
async def handle_r(event):
    await event.answer()
    await cunt_rm(event) 
@ABH.on(events.CallbackQuery(data=b"m"))
async def handle_r(event):
    await event.answer()
    await cunt_m(event)
@ABH.on(events.NewMessage(pattern='^رجب$'))
async def cunt_r(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 12, 21)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^شعبان$'))
async def cunt_sh(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2026, 2, 2)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^رمضان$'))
async def cunt_rm(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 3, 1)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
@ABH.on(events.NewMessage(pattern='^محرم$'))
async def cunt_m(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 6, 26)
    days_difference = (t2 - t.date()).days
    if days_difference < 0:
        await event.reply("الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1")
    else:
        await event.reply(f"باقي {days_difference} ايام")
        
print("Bot is running...")
ABH.run_until_disconnected()
