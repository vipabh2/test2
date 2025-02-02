from telethon import events, TelegramClient, Button
import datetime
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# تخزين تواريخ الأشهر الهجرية (يجب تحديثها سنويًا)
dates = {
    "رجب": datetime.date(2025, 12, 21),
    "شعبان": datetime.date(2026, 2, 2),
    "رمضان": datetime.date(2025, 3, 1),
    "محرم": datetime.date(2025, 6, 26)
}

# **متغير واحد يحتوي على الأزرار لتسهيل التعديل**
buttons_list = [
    [Button.inline("محرم", b"m"), Button.inline("رمضان", b"rm")],
    [Button.inline("شعبان", b"sh"), Button.inline("رجب", b"r")]
]

@ABH.on(events.NewMessage(pattern='^/dates$'))
async def show_months(event):
    await event.respond("اختر الشهر المناسب 👇", buttons=buttons_list)

@ABH.on(events.CallbackQuery)
async def handle_callback(event):
    data = event.data.decode("utf-8")  # تحويل البيانات من bytes إلى string
    month_map = {"m": "محرم", "rm": "رمضان", "sh": "شعبان", "r": "رجب"}
    
    if data in month_map:
        await calculate_days(event, month_map[data])

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
