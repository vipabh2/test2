from telethon import TelegramClient, events
import requests
import asyncio
from datetime import datetime, time
import pytz
import os

# تحميل بيانات API من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إعدادات الموقع والوقت
city = 'Baghdad'  
country = 'Iraq'  
method = 0  
timezone = 'Asia/Baghdad'

# تشغيل البوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# أسماء الصلوات بالعربي
prayer_names = {
    'Fajr': 'الفجر',
    'Dhuhr': 'الظهر',
    'Asr': 'العصر',
    'Maghrib': 'المغرب',
    'Isha': 'العشاء'
}

# تخزين أوقات الصلاة
prayer_times = {}

async def fetch_prayer_times():
    """جلب أوقات الصلاة مرة واحدة يوميًا"""
    global prayer_times
    url = f'http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method={method}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # إذا كان هناك خطأ في الـ API راح يرمي استثناء
        data = response.json()
        timings = data['data']['timings']

        tz = pytz.timezone(timezone)
        today = datetime.now(tz).date()

        # تحويل الأوقات إلى كائنات datetime.time
        prayer_times = {
            prayer: datetime.strptime(timings[prayer], "%H:%M").time()
            for prayer in prayer_names
        }
        print("✅ تم تحديث أوقات الصلاة:", prayer_times)
    except requests.RequestException as e:
        print("⚠️ خطأ أثناء جلب أوقات الصلاة:", str(e))

async def check_prayer_times(chat_id):
    """التحقق من أوقات الصلاة وإرسال تنبيه عند وقت الصلاة"""
    tz = pytz.timezone(timezone)
    
    while True:
        now = datetime.now(tz).time()
        
        for prayer, prayer_time in prayer_times.items():
            if now.hour == prayer_time.hour and now.minute == prayer_time.minute:
                prayer_name = prayer_names.get(prayer, prayer)
                audio_file = "https://t.me/najauaha/281"
                message = f"**حان الآن موعد صلاة {prayer_name}**\n" \
                          "```عن الإمام الصادق (عليه السلام) عن الرسول (صلى الله عليه وآله وسلم) قال: لاينال شفاعتي من إستخفّ بصلاتهِ```"
                await ABH.send_file(chat_id, audio_file, caption=message)
        
        await asyncio.sleep(60)

async def daily_prayer_update():
    """تحديث أوقات الصلاة كل 24 ساعة"""
    while True:
        await fetch_prayer_times()
        await asyncio.sleep(86400)  # إعادة التحديث كل 24 ساعة

# تشغيل تحديث الأوقات تلقائيًا عند بدء البوت
ABH.loop.create_task(daily_prayer_update())

# تخزين المهمة حتى نقدر نلغيها لاحقًا
prayer_task = None

@ABH.on(events.NewMessage(pattern='.تفعيل الاذان'))
async def enable_adhan(event):
    global prayer_task
    chat_id = event.chat_id
    
    if prayer_task is None:
        prayer_task = asyncio.create_task(check_prayer_times(chat_id))
        await event.reply("**᯽︙ تم تفعيل التنبيهات للصلوات الخمسة هنا **")
    else:
        await event.reply("**᯽︙ التنبيهات مفعلة بالفعل **")

@ABH.on(events.NewMessage(pattern='.تعطيل الاذان'))
async def disable_adhan(event):
    global prayer_task
    if prayer_task:
        prayer_task.cancel()
        prayer_task = None
        await event.reply("**᯽︙ تم تعطيل التنبيهات للصلوات الخمسة **")
    else:
        await event.reply("**᯽︙ التنبيهات غير مفعلة **")

with ABH:
    ABH.run_until_disconnected()
