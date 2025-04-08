from telethon import TelegramClient, events
import subprocess
import os

# قراءة متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء مجلد التنزيل إن لم يكن موجوداً
os.makedirs('downloads', exist_ok=True)

# تهيئة العميل
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# دالة لتحميل الفيديو باستخدام you-get عبر subprocess مع تمرير الكوكيز
def download_youtube_video(url):
    # تحديد المسار لتحميل الفيديو
    output_path = 'downloads/%(title)s.%(ext)s'
    
    # تمرير ملف الكوكيز مع الأمر
    cookies_file = '/path/to/your/cookies.txt'  # ضع مسار ملف الكوكيز هنا
    
    command = f"you-get -o downloads --cookies {cookies_file} {url}"
    
    try:
        # تنفيذ الأمر عبر subprocess
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)  # طباعة مخرجات الأمر
        print(result.stderr)  # طباعة الأخطاء إن وجدت
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل الأمر: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        raise

    # تحديد الملف بعد التحميل (يمكن تعديل المسار حسب الحاجة)
    file_name = os.path.join('downloads', f"{url.split('=')[-1]}.mp4")
    
    return file_name

# الاستماع للروابط
@bot.on(events.NewMessage(pattern=r'https?://(?:www\.)?youtube\.com/watch\?v=.*|https?://youtu\.be/.*'))
async def handler(event):
    url = event.raw_text
    await event.respond("⏳ جاري تحميل الفيديو من YouTube...")

    try:
        file_path = download_youtube_video(url)
        await event.respond("✅ تم التحميل، جارٍ الإرسال...")
        await bot.send_file(event.chat_id, file_path)
        os.remove(file_path)  # تنظيف الملف بعد الإرسال
    except Exception as e:
        await event.respond(f"❌ خطأ أثناء التحميل: {str(e)}")

# تشغيل البوت
print("✅ البوت يعمل الآن باستخدام you-get لتحميل الفيديو.")
bot.run_until_disconnected()
