from telethon import TelegramClient, events
import os

# جلب البيانات من المتغيرات البيئية
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل العميل
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("👋 أهلاً بك! أنا بوت تليثون.\n\nاستخدم /help لعرض الأوامر المتاحة.")
ABH
# أمر /help لعرض قائمة الأوامر
@ABH.on(events.NewMessage(pattern="/help"))
async def help(event):
    help_text = """📌 **قائمة الأوامر:**  
    🔹 `/start` - بدء المحادثة  
    🔹 `/help` - عرض قائمة الأوامر  
    🔹 `/alert [نص]` - إرسال تنبيه لكل المجموعات  
    🔹 الرد على رسالة مع `/alert` لإرسالها للمجموعات  
    """
    await event.reply(help_text)

# أمر /alert لإرسال التنبيه لكل المجموعات مع دعم النص أو الرد
@ABH.on(events.NewMessage(pattern="/alert"))
async def send_alert(event):
    sender = await event.get_sender()
    
    # استخراج الرسالة المطلوبة
    message_text = None
    
    if event.reply_to_msg_id:  # إذا تم الرد على رسالة
        replied_msg = await event.get_reply_message()
        message_text = replied_msg.text
    else:  # إذا تم كتابة نص بعد الأمر
        command_parts = event.raw_text.split(maxsplit=1)
        if len(command_parts) > 1:
            message_text = command_parts[1]

    # إذا لم يكن هناك نص، أطلب من المستخدم إدخال رسالة
    if not message_text:
        await event.reply("⚠️ يرجى الرد على رسالة أو كتابة نص بعد `/alert`.")
        return

    await event.reply("🚀 جاري إرسال التنبيه إلى جميع المجموعات...")

    async for dialog in ABH.iter_dialogs():
        if dialog.is_group:
            try:
                await ABH.send_message(dialog.id, f"📢 **تنبيه مهم:**\n{message_text}")
                print(f"تم إرسال التنبيه إلى: {dialog.title}")
            except Exception as e:
                print(f"خطأ عند الإرسال إلى {dialog.title}: {e}")

    await event.reply("✅ تم إرسال التنبيه لكل المجموعات!")

# تشغيل البوت
print("✅ البوت يعمل...")
ABH.run_until_disconnected()
