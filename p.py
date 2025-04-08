from telethon import TelegramClient, events
import yt_dlp
import os

# قراءة متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء مجلد التنزيل إن لم يكن موجوداً
os.makedirs('downloads', exist_ok=True)

# تهيئة العميل
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# دالة لتحميل الفيديو باستخدام yt-dlp
def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',  # تحميل أفضل جودة
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # تحديد المجلد ومسار التحميل
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج معلومات الفيديو
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)  # الحصول على اسم الملف الذي تم تحميله
    except Exception as e:
        print(f"❌ خطأ أثناء التحميل: {str(e)}")
        return None

# الاستماع للروابط
@bot.on(events.NewMessage(pattern=r'https?://(?:www\.)?youtube\.com/watch\?v=.*|https?://youtu\.be/.*'))
async def handler(event):
    url = event.raw_text
    await event.respond("⏳ جاري تحميل الفيديو من YouTube...")

    try:
        file_path = download_youtube_video(url)
        if file_path:
            await event.respond("✅ تم التحميل، جارٍ الإرسال...")
            await bot.send_file(event.chat_id, file_path)
            os.remove(file_path)  # تنظيف الملف بعد الإرسال
        else:
            await event.respond("❌ فشل التحميل.")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء التحميل: {str(e)}")

# تشغيل البوت
print("✅ البوت يعمل الآن باستخدام yt-dlp لتحميل الفيديو.")
bot.run_until_disconnected()
