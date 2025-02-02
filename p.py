from telethon import events, TelegramClient, Button
import datetime
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# تحديد تواريخ الأشهر الهجرية (يجب تحديثها سنويًا)
dates = {
    "رجب": datetime.date(2025, 12, 21),
    "شعبان": datetime.date(2026, 2, 2),
    "رمضان": datetime.date(2025, 3, 1),
    "محرم": datetime.date(2025, 6, 26)
}

@ABH.on(events.NewMessage(pattern='^/dates$'))
async def show_months(event):
    buttons = [
        [Button.inline("محرم", b"m"), Button.inline("رمضان", b"rm")],
        [Button.inline("شعبان", b"sh"), Button.inline("رجب", b"r")]
    ]
    await event.respond("اختر الشهر المناسب 👇", buttons=buttons)

@ABH.on(events.CallbackQuery(data=b"r"))
async def handle_r(event):
    await calculate_days(event, "رجب")

@ABH.on(events.CallbackQuery(data=b"sh"))
async def handle_sh(event):
    await calculate_days(event, "شعبان")

@ABH.on(events.CallbackQuery(data=b"rm"))
async def handle_rm(event):
    await calculate_days(event, "رمضان")

@ABH.on(events.CallbackQuery(data=b"m"))
async def handle_m(event):
    await calculate_days(event, "محرم")

async def calculate_days(event, month):
    today = datetime.date.today()
    target_date = dates.get(month)

    if not target_date:
        await event.respond("حدث خطأ في جلب التاريخ، تأكد من صحة البيانات.")
        return

    days_difference = (target_date - today).days

    if days_difference < 0:
        await event.respond(f"الشهر قد بدأ!\nيا مطوري، حدث الكود @k_4x1")
    else:
        await event.respond(f"بقي {days_difference} يومًا على شهر {month}.")

print("Bot is running...")
ABH.run_until_disconnected()
