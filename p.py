from telethon import TelegramClient, events
import os
import json

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تشغيل العميل
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# ملف لحفظ معرفات المحادثات
GROUPS_FILE = "dialogs.json"

# معرف المحادثة المستهدفة (التي سيتم إرسال الرسائل إليها)
TARGET_CHAT_ID = 1910015590

# تحميل المحادثات من الملف
def load_dialogs():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return set(json.load(f))
    return set()

# حفظ المحادثات إلى الملف
def save_dialogs():
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(dialog_ids), f)

# قائمة المحادثات المخزنة
dialog_ids = load_dialogs()

# إرسال رسالة إلى المحادثة المستهدفة
async def send_message_to_target_chat(message):
    try:
        await ABH.send_message(TARGET_CHAT_ID, message)
    except Exception as e:
        print(f"فشل إرسال الرسالة إلى المحادثة المستهدفة: {e}")

# تحديث المحادثات عند تلقي رسالة جديدة
@ABH.on(events.NewMessage)
async def update_dialogs(event):
    global dialog_ids
    chat = await event.get_chat()
    if chat.id not in dialog_ids:
        try:
            dialog_ids.add(chat.id)
            save_dialogs()
            success_message = f"تم إضافة المحادثة الجديدة: {chat.id} - {chat.title}"
            await send_message_to_target_chat(success_message)
        except Exception as e:
            error_message = f"فشل إضافة المحادثة: {chat.id} - {e}"
            await send_message_to_target_chat(error_message)

# إرسال التنبيه إلى جميع المحادثات
@ABH.on(events.NewMessage(pattern="/alert"))
async def send_alert(event):
    message_text = None
    # التأكد من أن المرسل هو المستخدم المستهدف
    if event.reply_to_msg_id and event.sender_id == 1910015590:
        replied_msg = await event.get_reply_message()
        message_text = replied_msg.text
    else:
        command_parts = event.raw_text.split(maxsplit=1)
        if len(command_parts) > 1:
            message_text = command_parts[1]

    if not message_text:
        await event.reply("⚠️ يرجى الرد على رسالة أو كتابة نص بعد `/alert`. ")
        return

    await event.reply(f"🚀 جاري إرسال التنبيه إلى {len(dialog_ids)} محادثة...")

    # إرسال التنبيه إلى جميع المحادثات
    for dialog_id in dialog_ids:
        try:
            await ABH.send_message(dialog_id, f"**{message_text}**")
            success_message = f"✅ تم الإرسال إلى: {dialog_id}"
            await send_message_to_target_chat(success_message)
        except Exception as e:
            error_message = f"❌ فشل الإرسال إلى {dialog_id}: {e}"
            await send_message_to_target_chat(error_message)

    await event.reply("تم إرسال التنبيه لجميع المحادثات!")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
