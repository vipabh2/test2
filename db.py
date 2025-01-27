import uuid  # استيراد مكتبة uuid
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
                reciver = await client.get_entity(username)  # الحصول على كيان المستلم
                reciver_id = reciver.id  # استخراج معرف المستلم
                
                # إنشاء معرف فريد للهمسة باستخدام uuid4
                whisper_id = str(uuid.uuid4())
                
                # تخزين الهمسة في قاعدة البيانات
                store_whisper(whisper_id, sender, reciver_id, username, message)

                # إنشاء الرد للمستخدم
                result = builder.article(
                    title='اضغط لإرسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى ({username})",
                    buttons=[
                        Button.inline(
                            text='📩 اضغط لعرض الهمسة', 
                            data=f'send:{username}:{message}:{sender}:{whisper_id}'
                        )
                    ]
                )
            except Exception as e:
                result = builder.article(
                    title='خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                    text=f'⚠️ خطأ: {str(e)}'
                )
        else:
            # عرض رسالة خطأ عند عدم استخدام التنسيق الصحيح
            result = builder.article(
                title='خطأ في التنسيق',
                description="يرجى استخدام التنسيق الصحيح: <message> @username",
                text='⚠️ التنسيق غير صحيح. يرجى إرسال الهمسة بالتنسيق: <message> @username'
            )
        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        try:
            # فك البيانات المرسلة
            _, username, message, sender_id, whisper_id = data.split(':', 4)
            
            # استرجاع الهمسة باستخدام المعرف الفريد
            whisper = get_whisper(whisper_id)

            if whisper:
                if event.sender_id == whisper.sender_id or event.sender_id == whisper.reciver_id:
                    # إنشاء معرف جديد عند عرض الرسالة
                    new_whisper_id = str(uuid.uuid4())
                    store_whisper(new_whisper_id, whisper.sender_id, whisper.reciver_id, whisper.username, whisper.message)
                    
                    await event.answer(f"📩 همستك:\n\n{whisper.message}", alert=True)
                else:
                    await event.answer("❌ عزيزي الحشري، هذه الهمسة ليست موجهة إليك!", alert=True)
            else:
                await event.answer("⚠️ هذه الهمسة لم تعد متاحة أو قد تكون محذوفة.", alert=True)
        except Exception as e:
            # التعامل مع الأخطاء عند استرجاع الهمسة
            await event.answer(f"🚨 حدث خطأ أثناء معالجة الطلب: {str(e)}", alert=True)

# تشغيل البوت حتى يتم إيقافه يدويًا
client.run_until_disconnected()
