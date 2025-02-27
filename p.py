from telethon import TelegramClient, events
import os
from youtubesearchpython import VideosSearch
import yt_dlp
from pathlib import Path

# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

# دالة للبحث في يوتيوب باستخدام youtubesearchpython
async def yt_search(query):
    search = VideosSearch(query, limit=1)  # البحث عن أول نتيجة
    results = search.result()

    if results['result']:
        return results['result'][0]['link']  # إرجاع رابط الفيديو
    return None

# دالة لتنزيل الفيديو باستخدام yt-dlp
async def download_video(url):
    ydl_opts = {
        'format': 'best',  # اختيار أفضل جودة
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # حفظ الفيديو في المجلد المناسب
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])
    return result

# إعداد الاتصال مع تليجرام باستخدام توكن البوت
@ABH.on(events.NewMessage(pattern=r'فيديو(?:\s|$)([\s\S]*)'))
async def _(event):
    "البحث عن الفيديو وإرساله للمستخدم"
    reply_to_id = await event.reply("⌔∮ جاري البحث عن الفيديو...")

    # استخراج الاستعلام من الرسالة
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    else:
        return await event.reply("⌔∮ يرجى الرد على ما تريد البحث عنه")

    # البحث في يوتيوب باستخدام مكتبة youtubesearchpython
    video_link = await yt_search(str(query))

    if not video_link:
        return await event.reply(f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`")

    # تنزيل الفيديو باستخدام yt-dlp
    await event.reply(f"⌔∮ تم العثور على الفيديو، جاري تحميله...")

    try:
        download_video(video_link)
    except Exception as e:
        return await event.reply(f"⌔∮ حدث خطأ أثناء تنزيل الفيديو: {str(e)}")

    # تحديد مكان الفيديو الذي تم تنزيله
    video_path = Path(f"downloads/{os.path.basename(video_link)}.mp4")

    if not video_path.exists():
        return await event.reply(f"⌔∮ عذرا لم استطع تنزيل الفيديو.")

    # إرسال الفيديو للمستخدم
    await event.reply("⌔∮ جاري إرسال الفيديو...")

    # إرسال الملف
    await event.client.send_file(
        event.chat_id,
        video_path,
        caption=f"**Title:** `{query}`",
        reply_to=reply_to_id
    )

    # حذف الفيديو بعد الإرسال
    if video_path.exists():
        os.remove(video_path)

# تشغيل البوت
ABH.run_until_disconnected()
