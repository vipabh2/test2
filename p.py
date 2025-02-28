from telethon import TelegramClient, events
import os
import json

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

GROUPS_FILE = "dialogs.json"
TARGET_CHAT_ID = 1910015590  # المعرف الثابت للمحادثة المستهدفة

# تحميل المحادثات المسجلة
def load_dialogs():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return set(json.load(f))
    return set()

# حفظ المحادثات المسجلة
def save_dialogs():
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(dialog_ids), f)

dialog_ids = load_dialogs()

# دالة لإرسال الأخطاء أو رسائل أخرى إلى المحادثة المستهدفة
async def send_message_to_target_chat(message):
    try:
        await ABH.send_message(TARGET_CHAT_ID, message)
    except Exception as e:
        print(f"فشل إرسال الرسالة إلى المحادثة المستهدفة: {e}")

# تحديث المحادثات التي لم يتم إضافتها بعد
@ABH.on(events.NewMessage)
async def update_dialogs(event):
    global dialog_ids
    chat = await event.get_chat()
    if chat.id not in dialog_ids:
        try:
            dialog_ids.add(chat.id)
            save_dialogs()
            success_message = f"تم إضافة المحادثة الجديدة: {chat.id} - {chat.title}"
            print(success_message)
            await send_message_to_target_chat(success_message)  # إرسال رسالة التأكيد إلى المحادثة المستهدفة
        except Exception as e:
            error_message = f"فشل إضافة المحادثة: {chat.id} - {e}"
            print(error_message)
            await send_message_to_target_chat(error_message)  # إرسال رسالة الخطأ إلى المحادثة المستهدفة

# إرسال التنبيه إلى جميع المحادثات
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
        await event.reply("⚠️ يرجى الرد على رسالة أو كتابة نص بعد `/alert`. ")
        return

    await event.reply(f"🚀 جاري إرسال التنبيه إلى {len(dialog_ids)} محادثة...")

    for dialog_id in dialog_ids:
        try:
            await ABH.send_message(dialog_id, f"**{message_text}**")
            print(f"✅ تم الإرسال إلى: {dialog_id}")
        except Exception as e:
            error_message = f"❌ فشل الإرسال إلى {dialog_id}: {e}"
            print(error_message)
            await send_message_to_target_chat(error_message)

    await event.reply(" تم إرسال التنبيه لجميع المحادثات!")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
