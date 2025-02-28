from telethon import TelegramClient, events
import os

# جلب البيانات من المتغيرات البيئية
api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# قائمة معرفات المجموعات (يجب إضافتها يدويًا)
group_ids = [-1001234567890, -1009876543210]  # ضع معرفات المجموعات هنا

# تشغيل العميل
ABH = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("👋 أهلاً بك! أنا بوت تليثون.\n\nاستخدم /help لعرض الأوامر المتاحة.")

@ABH.on(events.NewMessage(pattern="/help"))
async def help(event):
    help_text = """📌 **قائمة الأوامر:**  
    🔹 `/start` - بدء المحادثة  
    🔹 `/help` - عرض قائمة الأوامر  
    🔹 `/alert [نص]` - إرسال تنبيه لكل المجموعات  
    🔹 الرد على رسالة مع `/alert` لإرسالها للمجموعات  
    """
    await event.reply(help_text)

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
