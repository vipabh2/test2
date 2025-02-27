from telethon import TelegramClient, events
import os, re
import yt_dlp  # بدلاً من pytube

# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage())  
async def youtube_download(event):
    # الحصول على نص الرسالة
    message_text = event.message.text
    
    # البحث عن رابط يوتيوب في النص باستخدام تعبير عادي
    youtube_url_pattern = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+|https?://youtu\.be/[\w-]+)'
    match = re.search(youtube_url_pattern, message_text)
    
    if match:
        video_url = match.group(0)  # استخراج الرابط المتطابق
        await event.reply(f"🔍 جاري تحميل الفيديو من: {video_url}")

        try:
            # تحميل الفيديو باستخدام yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',  # تحميل أفضل جودة للصوت فقط
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'downloaded_audio.%(ext)s',  # حفظ الملف مؤقتًا باسم ثابت
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # التحقق مما إذا كان الملف موجودًا
            audio_file = "downloaded_audio.mp3"
            if os.path.exists(audio_file):
                await event.reply("✅ تم التحميل! جاري الإرسال...")
                await ABH.send_file(event.chat_id, audio_file, caption=f"🎵 فيديو: {video_url}")
                os.remove(audio_file)  # حذف الملف بعد الإرسال
            else:
                await event.reply("❌ لم يتم العثور على الملف!")

        except Exception as e:
            await event.reply(f"❌ حدث خطأ: {str(e)}")
    else:
        await event.reply("❌ لم يتم العثور على رابط يوتيوب في الرسالة.")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
