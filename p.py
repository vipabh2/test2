# bot.py
from telethon import TelegramClient, events, Button
from db import store_whisper, get_whisper  # استيراد الدوال من db.py

# إعدادات البوت
api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# معالجة الاستعلامات الواردة من البوت
@client.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text
    sender = event.sender_id
    if query.strip():
        parts = query.split(' ')
        if len(parts) >= 2:
            message = ' '.join(parts[:-1])
            username = parts[-1]

            if not username.startswith('@'):
                username = f'@{username}'

            try:
                reciver_id = await client.get_entity(username)  # الحصول على ID المستلم
                whisper_id = f"{sender}:{reciver_id.id}"  # إنشاء معرف خاص بالهمسة
                store_whisper(whisper_id, sender, reciver_id.id, username, message)

                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي ({username})",
                    buttons=[Button.inline(text='tap to see', data=f'send:{username}:{message}:{sender}:{whisper_id}')])
            except Exception as e:
                result = builder.article(
                    title='لرؤية المزيد حول الهمس',
                    description="همس",
                    text=f'خطأ: {str(e)}'
                )
        else:
            result = builder.article(
                title='خطأ في التنسيق',
                description="يرجى استخدام التنسيق الصحيح: @username <message>",
                text='التنسيق غير صحيح، يرجى إرسال الهمسة بالتنسيق الصحيح: @username <message>'
            )
        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        try:
            # تقسيم البيانات القادمة
            _, username, message_id, sender_id, whisper_id = data.split(':', 4)

            # استدعاء الهمسة باستخدام المعرف
            whisper = get_whisper(whisper_id)

            if whisper:
                # التحقق من صلاحيات الوصول
                if event.sender_id == whisper.sender_id or event.sender_id == whisper.reciver_id:
                    # إنشاء رابط الرسالة
                    link = f"https://t.me/{username}/{message_id}"

                    # إرسال رابط الرسالة كرد
                    await event.respond(f"رابط الهمسة: {link}")
                else:
                    # المستخدم ليس مرسل الهمسة أو مستقبلها
                    await event.respond("❌ عزيزي الحشري، هذه الهمسة ليست موجهة إليك!")
            else:
                # الهمسة غير موجودة
                await event.respond("⚠️ الهمسة غير موجودة أو قد تكون محذوفة.")
        except ValueError:
            # إذا كان هناك خطأ في تقسيم البيانات
            await event.respond("⚠️ البيانات غير صحيحة، تأكد من المدخلات.")
        except Exception as e:
            # أخطاء عامة
            await event.respond(f"🚨 حدث خطأ أثناء المعالجة: {str(e)}")


client.run_until_disconnected()
