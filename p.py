from telethon import TelegramClient, events
import yt_dlp

# إعدادات التليجرام
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='https://www.youtube.com/watch?v='))
async def download_video(event):
    url = event.message.text
    await event.reply("جاري تحميل الفيديو...")

    # إعدادات yt-dlp
    ydl_opts = {
        "format": "bestvideo+bestaudio",
        "outtmpl": "%(title)s.%(ext)s"
    }

    # تنزيل الفيديو باستخدام yt-dlp
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # الرد برسالة عند اكتمال التحميل
        await event.reply("✅ تم تحميل الفيديو بنجاح!")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ أثناء تحميل الفيديو: {e}")

# تشغيل البوت
client.run_until_disconnected()
