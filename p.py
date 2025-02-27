from telethon import TelegramClient, events
from pytube import YouTube
import os
import re

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
            # تحميل الفيديو باستخدام pytube
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()  # الحصول على أفضل جودة
            download_path = 'downloaded_video.mp4'  # حفظ الفيديو باسم ثابت
            stream.download(output_path='.', filename=download_path)

            # إرسال الفيديو للمستخدم
            await event.reply("✅ تم التحميل! جاري الإرسال...")
            await ABH.send_file(event.chat_id, download_path, caption=f"📹 فيديو: {yt.title}")
            
            os.remove(download_path)  # حذف الفيديو بعد الإرساء

        except Exception as e:
            await event.reply(f"❌ حدث خطأ: {str(e)}")
    else:
        await event.reply("❌ لم يتم العثور على رابط يوتيوب في الرسالة.")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
