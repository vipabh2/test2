from telethon import TelegramClient, events
import os

# جلب بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تشغيل العميل
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# قائمة معرفات المجموعات
group_ids = set()

# وظيفة لاكتشاف جميع المجموعات وإضافتها إلى القائمة
async def discover_groups():
    async for dialog in ABH.iter_dialogs():
        if dialog.is_group:  # التأكد من أن المحادثة مجموعة وليس خاص
            group_ids.add(dialog.id)
            print(f"✅ اكتشفنا مجموعة: {dialog.title} - {dialog.id}")

# عند تشغيل البوت، يقوم بفحص المجموعات تلقائيًا
@ABH.on(events.NewMessage(pattern="/scan"))
async def scan_groups(event):
    await event.reply("🔍 جاري البحث عن جميع المجموعات التي يمكنني الوصول إليها...")
    await discover_groups()
    await event.reply(f"✅ تم تسجيل {len(group_ids)} مجموعة!")

# عند إضافة البوت إلى مجموعة جديدة، يتم تسجيلها تلقائيًا
@ABH.on(events.ChatAction)
async def join_group(event):
    if event.user_added and event.user_id == (await ABH.get_me()).id:
        group_ids.add(event.chat_id)
        print(f"✅ تم تسجيل المجموعة الجديدة: {event.chat_id}")

# أمر /alert لإرسال التنبيه لكل المجموعات
@ABH.on(events.NewMessage(pattern="/alert"))
async def send_alert(event):
    message_text = None

    if event.reply_to_msg_id:
        replied_msg = await event.get_reply_message()
        message_text = replied_msg.text
    else:
        command_parts = event.raw_text.split(maxsplit=1)
        if len(command_parts) > 1:
            message_text = command_parts[1]

    if not message_text:
        await event.reply("⚠️ يرجى الرد على رسالة أو كتابة نص بعد `/alert`.")
        return

    await event.reply("🚀 جاري إرسال التنبيه إلى جميع المجموعات...")

    for group_id in group_ids:
        try:
            await ABH.send_message(group_id, f"📢 **تنبيه مهم:**\n{message_text}")
            print(f"✅ تم الإرسال إلى: {group_id}")
        except Exception as e:
            print(f"❌ فشل الإرسال إلى {group_id}: {e}")

    await event.reply("✅ تم إرسال التنبيه لكل المجموعات!")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
