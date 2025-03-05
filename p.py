from telethon import TelegramClient, events
import yt_dlp, os
import asyncio

api_id = os.getenv('API_ID')      # API_ID
api_hash = os.getenv('API_HASH')  # API_HASH
bot_token = os.getenv('BOT_TOKEN') # BOT_TOKEN

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
            "outtmpl": "%(title)s.%(ext)s",
            # تأكد من استخدام الكوكيز إذا كانت متاحة
            "cookies": "cookies.txt",  # وضع مسار ملف الكوكيز إذا كنت بحاجة إليه
        }

        # تنزيل الفيديو باستخدام yt-dlp
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # الرد برسالة عند اكتمال التحميل
            await event.reply("✅ تم تحميل الفيديو بنجاح!")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء تحميل الفيديو: {e}")

# تشغيل البوت للاستماع للرسائل بشكل مستمر
client.run_until_disconnected()
