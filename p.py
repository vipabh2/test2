from telethon import TelegramClient, events
import yt_dlp
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
# تهيئة العميل
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# دالة تحميل فيديو من يوتيوب
def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# الاستماع للرسائل
@bot.on(events.NewMessage(pattern=r'https?://(?:www\.)?youtube\.com/watch\?v=.*|https?://youtu\.be/.*'))
async def handler(event):
    url = event.raw_text
    await event.respond("⏳ جاري تحميل الفيديو من YouTube...")

    try:
        file_path = download_youtube_video(url)
        await event.respond("✅ تم التحميل. جارٍ الإرسال...")
        await bot.send_file(event.chat_id, file_path)
        os.remove(file_path)  # تنظيف الملف بعد الإرسال
    except Exception as e:
        await event.respond(f"❌ حدث خطأ أثناء التحميل: {str(e)}")

# بدء البوت
print("✅ البوت يعمل الآن.")
bot.run_until_disconnected()
