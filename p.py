from telethon import TelegramClient, events, Button
import random, os, yt_dlp

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r'يوت (.+)'))  
async def youtube_download(event):
    search_query = event.pattern_match.group(1)  # استخراج اسم البحث من الرسالة
    
    await event.reply("🔍 جاري البحث عن: " + search_query)

    # إعدادات تحميل الصوت
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',  # حفظ الملف مؤقتًا باسم ثابت
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{search_query}"])  # تحميل أول نتيجة فقط
        
        await event.reply("✅ تم التحميل! جاري الإرسال...")
        
        # إرسال الملف الصوتي للمستخدم
        await ABH.send_file(event.chat_id, "downloaded_audio.mp3", caption=f"🎵 {search_query}")

    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()

