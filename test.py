from telethon import TelegramClient, events, Button

# إعداد البوت
api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# تخزين الهمسات في ذاكرة مؤقتة
whispers = {}

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    global whispers
    builder = event.builder
    query = event.text

    if query.strip():  # التأكد من أن النص ليس فارغًا
        parts = query.split(' ')
        if len(parts) >= 2:  # التأكد من أن التنسيق يحتوي على رسالة واسم مستخدم
            message = ' '.join(parts[:-1])  # الرسالة
            username = parts[-1]  # اسم المستخدم

            # إضافة @ إذا لم تكن موجودة
            if not username.startswith('@'):
                username = f'@{username}'
            
            try:
                user_entity = await client.get_entity(username)

                # تخزين الهمسة مع معلومات المرسل والمستقبل
                whispers[event.sender_id] = {"username": username, "message": message}

                # عرض خيار إرسال الهمسة
                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"تم إنشاء همسة سرية إلى {username}. فقط المرسل والمستقبل يمكنهم رؤيتها.",
                    buttons=[
                        [Button.inline(text='عرض الهمسة', data=f'send:{event.sender_id}:{username}')]
                    ]
                )
            except Exception as e:
                # في حال لم يتم العثور على الكيان
                result = builder.article(
                    title='حدث خطأ',
                    description=str(e),
                    text=f'حدث خطأ: {str(e)}'
                )
        else:
            # في حال كان التنسيق غير صحيح
            result = builder.article(
                title='خطأ في التنسيق',
                description='يرجى استخدام التنسيق الصحيح: @games_abh <message> @<username>',
                text='خطأ في التنسيق: يرجى استخدام التنسيق الصحيح: @games_abh <message> @<username>'
            )

        # إرسال النتيجة
        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    global whispers
    data = event.data.decode('utf-8')

    if data.startswith('send:'):
        sender_id, username = data.split(':')[1:]
        sender_id = int(sender_id)  # تحويل معرف المرسل إلى عدد صحيح

        # التحقق إذا كان المستخدم الحالي هو المرسل أو المستقبل
        if event.sender_id == sender_id or f"@{event.sender.username}" == username:
            whisper = whispers.get(sender_id, None)
            if whisper and whisper["username"] == username:
                await event.answer(f"الرسالة: {whisper['message']}", alert=True)
            else:
                await event.answer("هذه الهمسة غير متوفرة.", alert=True)
        else:
            # إذا كان المستخدم الحالي ليس المرسل أو المستقبل
            await event.answer("لا يمكنك عرض هذه الهمسة.", alert=True)

client.run_until_disconnected()
