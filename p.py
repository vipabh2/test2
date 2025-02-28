from telethon import TelegramClient, events
import os
import json

# جلب بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تشغيل العميل
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# ملف لتخزين معرفات المجموعات
GROUPS_FILE = "groups.json"

# تحميل معرفات المجموعات من الملف
def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return set(json.load(f))
    return set()

# حفظ معرفات المجموعات إلى الملف
def save_groups():
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(group_ids), f)

# قائمة معرفات المجموعات
group_ids = load_groups()

# عند إضافة البوت إلى مجموعة، يتم تسجيلها تلقائيًا
@ABH.on(events.ChatAction)
async def join_group(event):
    if event.user_added and event.user_id == (await ABH.get_me()).id:
        group_ids.add(event.chat_id)
        save_groups()
        print(f"✅ تم تسجيل المجموعة الجديدة: {event.chat.title} - {event.chat_id}")
        await event.reply("✅ تم تسجيل هذه المجموعة! استخدم /alert لإرسال تنبيهات.")

# أمر /alert لإرسال التنبيه لكل المجموعات المسجلة
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

    await event.reply(f"🚀 جاري إرسال التنبيه إلى {len(group_ids)} مجموعة...")

    for group_id in group_ids:
        try:
            await ABH.send_message(group_id, f"📢 **تنبيه مهم:**\n{message_text}")
            print(f"✅ تم الإرسال إلى: {group_id}")
        except Exception as e:
            print(f"❌ فشل الإرسال إلى {group_id}: {e}")

    await event.reply("✅ تم إرسال التنبيه لكل المجموعات!")

print("✅ البوت يعمل...")
ABH.run_until_disconnected()
