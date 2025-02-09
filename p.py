from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonCallback
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('session_name', api_id, api_hash)

# متغيرات عامة لتخزين معلومات المستخدم
user = None
uid = None

@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(event):
    global user, uid
    uid = event.sender_id  # تخزين معرّف المستخدم الذي أرسل الأمر
    user_id = event.pattern_match.group(1)
    
    if not user_id:
        await event.reply("استخدم الأمر كـ `كشف ايدي 1910015590`")
        return
    
    try:
        user = await event.client.get_entity(int(user_id))
    except Exception as e:
        return await event.reply(f"لا يوجد حساب بهذا الآيدي...")
    
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.reply(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])

@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    global user, uid
    sender_id = event.sender_id  # معرّف المستخدم الذي ضغط على الزر
    
    # التحقق من أن المستخدم الذي ضغط على الزر هو نفسه الذي أرسل الأمر
    if sender_id != uid:
        await event.answer("⚠️ أنت لست المستخدم الذي أرسل الأمر!", alert=True)
        return
    
    # إذا كان المستخدم هو نفسه، قم بتعديل الرسالة وإرسال الرابط فقط
    await event.edit(f"⌔︙رابط المستخدم: tg://user?id={user.id}")

ABH.start(bot_token=bot_token)
ABH.run_until_disconnected()
