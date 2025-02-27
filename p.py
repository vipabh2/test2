
from telethon import TelegramClient, events
import os
import base64
from pathlib import Path
# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)




# إعداد الاتصال مع تليجرام باستخدام توكن البوت

@ABH.on(events.NewMessage(pattern=r'فيديو(?:\s|$)([\s\S]*)'))
async def _(event):
    "To search video songs"
    reply_to_id = await event.reply("⌔∮ جاري البحث عن الفيديو...")

    # استخراج الاستعلام من الرسالة
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    else:
        return await event.reply("⌔∮ يرجى الرد على ما تريد البحث عنه")

    # دالة وهمية `yt_search` للبحث في يوتيوب - يجب استبدالها بالبحث الفعلي
    video_link = await yt_search(str(query))

    # تحقق من وجود رابط الفيديو
    if not url(video_link):
        return await event.reply(f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`")

    # تنزيل الفيديو باستخدام أوامر النظام
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    name_cmd = f"command_to_get_video {video_link}"  # استبدل بـ الأمر الفعلي
    video_cmd = f"command_to_download_video {video_link}"  # استبدل بـ الأمر الفعلي
    
    # تنفيذ الأوامر وتحميل الفيديو
    try:
        stderr = (await _catutils.runcmd(video_cmd))[1]
        if stderr:
            return await event.reply(f"**Error :** `{stderr}`")
        catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
        if stderr:
            return await event.reply(f"**Error :** `{stderr}`")
        catname = os.path.splitext(catname)[0]
        vsong_file = Path(f"{catname}.mp4")
    except:
        pass

    # التحقق من وجود الفيديو
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await event.reply(f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`")

    # إرسال الفيديو للمستخدم
    await event.reply("**⌔∮ جاري الارسال انتظر قليلا**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    
    title = catname.replace("./temp/", "").replace("_", "|")
    
    # إرسال الملف
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        caption=f"**Title:** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    
    # حذف الملفات المؤقتة
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)

# تشغيل البوت
# بدء البوت
ABH.run_until_disconnected()
