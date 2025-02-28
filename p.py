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

# قائمة معرفات المجموعات المخزنة
group_ids = load_groups()

# 🔍 **فحص المجموعات وإضافة المشرف منها فقط**
async def scan_groups():
    global group_ids
    group_ids.clear()  # إعادة تعيين القائمة

    async for dialog in ABH.iter_dialogs():
        if dialog.is_group:  # تأكد أن المحادثة مجموعة
            try:
                chat = await ABH.get_entity(dialog.id)
                if chat.admin_rights:  # تحقق من أن البوت مشرف في هذه المجموعة
                    group_ids.add(dialog.id)
                    print(f"✅ البوت مشرف في المجموعة: {chat.title} - {chat.id}")
            except Exception as e:
                print(f"❌ فشل التحقق من {dialog.title}: {e}")

    save_groups()
    print(f"📌 تم حفظ {len(group_ids)} مجموعة.")

# 🛠️ **أمر لتحديث قائمة المجموعات المشرف فيها**
@ABH.on(events.NewMessage(pattern="/scan"))
async def update_groups(event):
    await event.reply("🔄 جاري تحديث قائمة المجموعات...")
    await scan_groups()
    await event.reply(f"✅ تم تحديث القائمة، البوت مشرف في {len(group_ids)} مجموعة.")

# 📢 **إرسال تنبيه للمجموعات التي فيها البوت مشرف**
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

# تشغيل فحص المجموعات عند بدء تشغيل البوت
async def startup():
    print("🔍 جاري البحث عن المجموعات...")
    await scan_groups()

print("✅ البوت يعمل...")
ABH.loop.run_until_complete(startup())  # تنفيذ البحث عند بدء التشغيل
ABH.run_until_disconnected()
