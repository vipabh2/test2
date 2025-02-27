from telethon import TelegramClient, events
import os
import yt_dlp  # تأكد من تثبيت yt-dlp
from pathlib import Path
import base64

# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

# دالة للبحث في يوتيوب باستخدام yt-dlp
async def yt_search(query):
    ydl_opts = {
        'format': 'bestaudio/best',  # البحث عن أفضل جودة للصوت أو الفيديو
        'noplaylist': True,  # تعطيل البحث في قوائم التشغيل
        'quiet': True,  # إخفاء الرسائل
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # البحث في يوتيوب باستخدام الاستعلام المرسل
        result = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in result:
            # إرجاع رابط أول نتيجة من البحث
            return result['entries'][0]['url']
    return None

@ABH.on(events.NewMessage(pattern=r'فيديو(?:\s|$)([\s\S]*)'))
async def _(event):
    "To search video songs"
    reply_to_id = await event.reply("⌔∮ جاري البحث عن الفيديو...")

    # استخراج الاستعلام من الرسالة
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    else:
        return await event.reply("⌔∮ يرجى الرد على ما تريد البحث عنه")

    # البحث في يوتيوب باستخدام yt_search
    video_link = await yt_search(str(query))

    # تحقق من وجود رابط الفيديو
    if not video_link:
        return await event.reply(f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`")

    # تنزيل الفيديو باستخدام yt-dlp
    ydl_opts = {
        'format': 'best',  # الحصول على أفضل جودة للفيديو
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # تحديد مكان حفظ الفيديو
        'quiet': True  # إخفاء المخرجات
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])
    
    # تحديد اسم الملف الذي تم تنزيله
    video_file = Path(f"downloads/{query}.mp4")
    
    if not video_file.exists():
        return await event.reply(f"⌔∮ عذرا لم استطع تنزيل الفيديو لـ `{query}`")

    # إرسال الفيديو للمستخدم
    await event.reply("**⌔∮ جاري الارسال انتظر قليلا**")
    await event.client.send_file(
        event.chat_id,
        video_file,
        caption=f"**Title:** `{query}`",
        supports_streaming=True,
        reply_to=reply_to_id,
    )

    # حذف الملف المؤقت بعد الإرسال
    if video_file.exists():
        os.remove(video_file)

# تشغيل البوت
ABH.run_until_disconnected()
