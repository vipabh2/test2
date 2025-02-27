from telethon import TelegramClient, events
import os, yt_dlp

# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r'يوت (.+)'))  
async def youtube_download(event):
    search_query = event.pattern_match.group(1)  # استخراج اسم البحث من الرسالة
    await event.reply(f"🔍 جاري البحث عن: {search_query}")

    # إعدادات تحميل الصوت بدون كوكيز
    ydl_opts = {
        'format': 'bestaudio/best',  # تحميل أفضل جودة للصوت فقط
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',  # حفظ الملف مؤقتًا باسم ثابت
        'noplaylist': True,  # تعطيل تحميل قوائم التشغيل
        'extractor-args': {'youtube': {'player_client': ['web']}},  # فرض مشغل الويب لتجاوز الحماية
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }  # تغيير هوية المتصفح لخداع يوتيوب
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{search_query}"])  # تحميل أول نتيجة فقط
        
        # التحقق مما إذا كان الملف موجودًا
        audio_file = "downloaded_audio.mp3"
        if os.path.exists(audio_file):
            await event.reply("✅ تم التحميل! جاري الإرسال...")
            await ABH.send_file(event.chat_id, audio_file, caption=f"🎵 {search_query}")
            os.remove(audio_file)  # حذف الملف بعد الإرسال
        else:
            await event.reply("❌ لم يتم العثور على الملف!")

    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
