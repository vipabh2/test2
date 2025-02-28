from telethon import TelegramClient, events
import os
import json
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)
GROUPS_FILE = "dialogs.json"
def load_dialogs():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return set(json.load(f))
    return set()
def save_dialogs():
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(dialog_ids), f)
dialog_ids = load_dialogs()
@ABH.on(events.NewMessage)
async def update_dialogs(event):
    global dialog_ids
    chat = await event.get_chat()
    if chat.id not in dialog_ids:
        try:
            dialog_ids.add(chat.id)
            save_dialogs()
            print(f"تم إضافة المحادثة: {chat.id}")
        except Exception as e:
            print(f"فشل إضافة المحادثة: {chat.id} - {e}")
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
    await event.reply(f"🚀 جاري إرسال التنبيه إلى {len(dialog_ids)} محادثة...")
    for dialog_id in dialog_ids:
        try:
            await ABH.send_message(dialog_id, f"**{message_text}**")
            print(f"✅ تم الإرسال إلى: {dialog_id}")
        except Exception as e:
            print(f"❌ فشل الإرسال إلى {dialog_id}: {e}")
    await event.reply(" تم إرسال التنبيه لجميع المحادثات!")
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
