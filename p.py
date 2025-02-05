from telethon import TelegramClient, events, Button
import os, uuid
from db import get_whisper, store_whisper

# تحميل متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

if not all([api_id, api_hash, bot_token]):
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN must be set as environment variables")

# تشغيل البوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='/whisper'))
async def whisper_command(event):
    """يتم تفعيل الأمر فقط عند استلام رسالة مباشرة (وليس inline query)"""
    replied = await event.get_reply_message()
    sender = event.sender_id

    if replied:
        reciver_id = replied.sender_id  # إرسال الهمسة إلى الشخص الذي عليه الرد
        username = f'User({reciver_id})'
    else:
        parts = event.text.split(' ', 1)
        if len(parts) < 2:
            await event.reply("❌ استخدم الأمر كالتالي: `/whisper [الرسالة] @username` أو رد على شخص.")
            return

        message = parts[1]
        username = message.split()[-1]

        if username.startswith('@'):
            try:
                reciver = await ABH.get_entity(username)
                reciver_id = reciver.id
            except Exception as e:
                await event.reply(f"❌ خطأ: {str(e)}")
                return
        else:
            await event.reply("❌ تأكد من كتابة اسم المستخدم مع @ أو الرد على رسالة مباشرة.")
            return

    # إنشاء معرّف فريد للهمسة
    whisper_id = str(uuid.uuid4())
    store_whisper(whisper_id, sender, reciver_id, username, message)

    # إرسال زر لاستقبال الهمسة
    await event.reply(
        "📩 لديك همسة سرية!",
        buttons=[Button.inline("🫵🏾 اضغط لعرض الهمسة", data=f'send:{whisper_id}')]
    )

@ABH.on(events.CallbackQuery)
async def callback_query_handler(event):
    """التعامل مع استعراض الهمسة"""
    data = event.data.decode('utf-8')

    if data.startswith('send:'):
        whisper_id = data.split(':')[1]
        whisper = get_whisper(whisper_id)

        if whisper:
            if event.sender_id in [whisper.sender_id, whisper.reciver_id]:
                await event.answer(f"{whisper.message}", alert=True)
            else:
                await event.answer("❌ هذه الهمسة ليست لك!", alert=True)

print("Bot is running...")
ABH.run_until_disconnected()
