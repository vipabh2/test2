from telethon import TelegramClient, events, Button
import os
from collections import defaultdict

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# قاموس لتخزين بيانات التصويت لكل رسالة
votes = defaultdict(lambda: {"like": 0, "dislike": 0, "text": "", "voters": set()})

@client.on(events.NewMessage(pattern=r'تصويت\s+(.+)'))
async def my_event_handler(event):
    match = event.pattern_match
    sender_id = event.sender_id

    if match and sender_id != 1910015590:
        text = match.group(1)  # استخراج نص التصويت
        message_id = event.message.id  # الحصول على معرف الرسالة

        # تخزين بيانات التصويت
        votes[message_id] = {"like": 0, "dislike": 0, "text": text, "voters": set()}

        # إنشاء الأزرار مع معرف الرسالة
        buttons = [
            [Button.inline(f"👍 0", f"yes_{message_id}".encode())],
            [Button.inline(f"👎 0", f"no_{message_id}".encode())]
        ]

        await event.respond(f"🗳 {text}", buttons=buttons)

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode()
    sender = await event.get_sender()  # إصلاح مشكلة sender_id في CallbackQuery
    user_id = sender.id
    
    if data.startswith("yes_") or data.startswith("no_"):
        message_id = int(data.split("_")[1])

        if message_id not in votes:
            await event.answer("❌ هذا التصويت لم يعد متاحًا!", alert=True)
            return

        # منع المستخدم من التصويت أكثر من مرة
        if user_id in votes[message_id]["voters"]:
            await event.answer("❌ لقد قمت بالتصويت بالفعل!", alert=False)
            return

        # تسجيل تصويت المستخدم
        votes[message_id]["voters"].add(user_id)

        if data.startswith("yes_"):
            votes[message_id]["like"] += 1
        else:
            votes[message_id]["dislike"] += 1

        # تحديث الأزرار مع القيم الجديدة
        buttons = [
            [Button.inline(f"👍 {votes[message_id]['like']}", f"yes_{message_id}".encode())],
            [Button.inline(f"👎 {votes[message_id]['dislike']}", f"no_{message_id}".encode())]
        ]

        # جلب نص التصويت الأصلي المخزن مسبقًا
        original_text = votes[message_id]["text"]

        # تحديث الرسالة بالأزرار الجديدة
        try:
            await event.edit(f"🗳 {original_text}", buttons=buttons)
        except Exception as e:
            print(f"خطأ أثناء تحديث التصويت: {e}")

client.run_until_disconnected()
