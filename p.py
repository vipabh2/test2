from telethon import TelegramClient, events
import yt_dlp, os

# جلب معلومات API من المتغيرات البيئية
api_id = os.getenv('API_ID')      # API_ID
api_hash = os.getenv('API_HASH')  # API_HASH
bot_token = os.getenv('BOT_TOKEN') # BOT_TOKEN

# مسار ملف الكوكيز
cookies_path = "موارد/cookies.txt"

# تشغيل العميل
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage())
async def download_video(event):
    url = event.message.text

    # التحقق مما إذا كان الرابط من يوتيوب
    if "youtube.com/watch?v=" in url or "youtu.be/" in url:
        await event.reply("جاري تحميل الفيديو...")

        # إعدادات yt-dlp مع دعم الكوكيز
        ydl_opts = {
            "format": "bestvideo+bestaudio",
            "outtmpl": "%(title)s.%(ext)s",
            "cookies": cookies_path  # استخدام ملف الكوكيز
        }

        # تنزيل الفيديو باستخدام yt-dlp
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(info)

            # إرسال الفيديو بعد تحميله
            await event.reply("✅ تم تحميل الفيديو بنجاح! جارٍ الإرسال...")
            await event.respond(file=video_filename)

            # حذف الملف بعد الإرسال لتوفير المساحة
            os.remove(video_filename)
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء تحميل الفيديو: {e}")

# تشغيل البوت للاستماع للرسائل بشكل مستمر
client.run_until_disconnected()
