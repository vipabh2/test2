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

# دالة لتحميل الصوت باستخدام ytmdl عبر subprocess
def download_youtube_audio(url):
    # تحديد المسار لتحميل الملف
    output_path = 'downloads/%(title)s.mp3'
    
    # تنفيذ أمر ytmdl لتحميل الصوت
    command = f"ytmdl --output '{output_path}' {url}"
    
    # تنفيذ الأمر عبر subprocess
    subprocess.run(command, shell=True, check=True)

    # تحديد الملف بعد التحميل
    file_name = os.path.join('downloads', f"{url.split('=')[-1]}.mp3")
    
    return file_name

# الاستماع للروابط
@bot.on(events.NewMessage(pattern=r'https?://(?:www\.)?youtube\.com/watch\?v=.*|https?://youtu\.be/.*'))
async def handler(event):
    url = event.raw_text
    await event.respond("🎵 جاري تحميل الصوت من YouTube...")

    try:
        file_path = download_youtube_audio(url)
        await event.respond("✅ تم التحميل، جارٍ الإرسال...")
        await bot.send_file(event.chat_id, file_path)
        os.remove(file_path)  # تنظيف الملف بعد الإرسال
    except Exception as e:
        await event.respond(f"❌ خطأ أثناء التحميل: {str(e)}")

# تشغيل البوت
print("✅ البوت يعمل الآن باستخدام ytmdl لتحميل الصوت.")
bot.run_until_disconnected()
