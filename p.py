from telethon import TelegramClient, events
import os, yt_dlp

# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)


@ABH.on(events.NewMessage)
async def handler(event):
    # إذا كانت الرسالة تحتوي على رابط
    if event.text.startswith('http'):
        url = event.text.strip()
        await event.reply('جاري تحميل الفيديو...')

        # تحميل الفيديو باستخدام yt-dlp
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # حفظ الفيديو في مجلد "downloads"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

        # البحث عن الملف الذي تم تنزيله
        downloaded_file = ydl.prepare_filename(result[0])

        # إرسال الفيديو إلى المستخدم
        await event.reply('تم تحميل الفيديو! الآن أرسله لك...', file=downloaded_file)

# بدء البوت
ABH.run_until_disconnected()
