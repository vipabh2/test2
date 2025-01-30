
from telethon import TelegramClient, events
import requests
import asyncio
from datetime import datetime
import pytz
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
city = 'Baghdad' #هنا خلي محافظتك
country = 'Iraq' #هنا خلي دولتك
method = 0 #اذا چنت من المذهب الشيعي اتركه
timezone = 'Asia/Baghdad'  #هنا تحط المنطقة الزمنية لدولتك
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

prayer_names = {
    'Fajr': 'الفجر',
    'Dhuhr': 'الظهر',
    'Asr': 'العصر',
    'Maghrib': 'المغرب',
    'Isha': 'العشاء'
}

jok = None

def joker_prayer_times(city, country, method):
    url = f'http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method={method}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        timings = data['data']['timings']
        filtered_timings = {key: value for key, value in timings.items() if key in prayer_names}
        return filtered_timings
    else:
        return None

async def lMl10l(chat_id):
    tz = pytz.timezone(timezone)
    while True:
        now = datetime.now(tz).strftime("%H:%M")
        timings = joker_prayer_times(city, country, method)
        if timings:
            for prayer_name, prayer_time in timings.items():
                prayer_time = datetime.strptime(prayer_time, "%H:%M").time()
                aljoker_time = datetime.strptime(now, "%H:%M").time()
                if aljoker_time == prayer_time:
                    hussein_name = prayer_names.get(prayer_name, prayer_name)
                    joker_hussein = "https://t.me/najauaha/281"
                    joker = f"**حان الآن موعد صلاة {hussein_name}**\n``` عن الإمام الصادق (عليه السلام) عن الرسول (صلى الله عليه وآله وسلم) قال: لاينال شفاعتي من إستخفّ بصلاتهِ```"
                    await ABH.send_file(chat_id, joker_hussein, caption=joker)
        await asyncio.sleep(60)

@ABH.on(events.NewMessage(pattern='.تفعيل الاذان'))
async def joker(hussein):
    global jok
    try:
        chat_id = hussein.chat_id
        if jok is None:
            jok = asyncio.create_task(lMl10l(chat_id))
            await hussein.reply("**᯽︙ تم تفعيل التنبيهات للصلوات الخمسه هنا ** ")
        else:
            await hussein.reply("**᯽︙ التنبيهات مفعلة بالفعل ** ")
    except Exception as e:
        await hussein.reply(f"حدث خطأ: {str(e)}")

@ABH.on(events.NewMessage(pattern='.تعطيل الاذان'))
async def joker(hussein):
    global jok
    try:
        if jok:
            jok.cancel()
            jok = None
            await hussein.reply("**᯽︙ تم تعطيل التنبيهات للصلوات الخمسه **")
        else:
            await hussein.reply("**᯽︙ التنبيهات غير مفعلة **")
    except Exception as e:
        await hussein.reply(f"حدث خطأ: {str(e)}")

with ABH:
    ABH.run_until_disconnected()
