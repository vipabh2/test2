from telethon import TelegramClient, events
import yt_dlp
import os
import asyncio

# إعداد المتغيرات
api_id = os.getenv('API_ID')      # API_ID
api_hash = os.getenv('API_HASH')  # API_HASH
bot_token = os.getenv('BOT_TOKEN') # BOT_TOKEN

# إنشاء العميل للبوت
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage())
async def download_video(event):
    url = event.message.text

    # التحقق مما إذا كان الرابط من يوتيوب
    if "youtube.com/watch?v=" in url or "youtu.be/" in url:
        await event.reply("جاري تحميل الفيديو...")

        # إعدادات yt-dlp
        ydl_opts = {
            "format": "bestvideo+bestaudio",
            "outtmpl": "موارد/%(title)s.%(ext)s",  # تحديد المجلد الذي سيتم حفظ الفيديو فيه
            "noplaylist": True  # عدم تحميل القوائم التلقائية
        }

        # تنزيل الفيديو باستخدام yt-dlp
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # الرد برسالة عند اكتمال التحميل
            await event.reply("✅ تم تحميل الفيديو بنجاح!")
        except Exception as e:
            # الرد برسالة في حال حدوث خطأ
            await event.reply(f"❌ حدث خطأ أثناء تحميل الفيديو: {str(e)}")

# تشغيل البوت للاستماع للرسائل بشكل مستمر
client.run_until_disconnected()
