from telethon import TelegramClient, events, Button
from db import create_table, save_whisper

# إعداد قاعدة البيانات
create_table()  # إنشاء الجداول إذا لم تكن موجودة

# إعداد البوت
api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    global message, username
    builder = event.builder
    query = event.text

    if query.strip():  # التأكد من أن الاستعلام ليس فارغًا
        parts = query.split(' ')
        if len(parts) >= 2:  # التأكد من أن هناك رسالة واسم مستخدم
            message = ' '.join(parts[:-1])  # الرسالة هي كل النص عدا الجزء الأخير
            username = parts[-1]  # الجزء الأخير هو اسم المستخدم
            
            # إضافة @ إذا لم تكن موجودة
            if not username.startswith('@'):
                username = f'@{username}'
            
            try:
                # تحقق من الكيان
                user_entity = await client.get_entity(username)
                
                # التأكد أن المستخدم الحالي هو نفسه المستهدف
                if event.sender_id != user_entity.id:
                    await event.answer([], switch_pm='هذه الهمسة ليست موجهة لك!', switch_pm_param='no_access')
                    return

                # حفظ الهمسة في قاعدة البيانات
                save_whisper(message, event.sender_id, username)

                # إنشاء الهمسة باستخدام تنسيق Markdown
                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"**همسة سرية إلى** \n{username} \nالله يثخن اللبن عمي!",
                    buttons=[ 
                        [Button.inline(text='tap to see', data=f'send:{username}:{message}')]
                    ]
                )
            except Exception as e:
                # التعامل مع الخطأ إذا لم يتم العثور على الكيان
                result = builder.article(
                    title='حدث خطأ',
                    description="لم يتم العثور على المستخدم",
                    text='حدث خطأ أثناء محاولة إرسال الهمسة. يرجى المحاولة لاحقًا.'
                )
        else:
            # إذا كان التنسيق غير صحيح
            result = builder.article(
                title='خطأ في التنسيق',
                description='يرجى استخدام التنسيق الصحيح: <message> @<username>',
                text='الرجاء إرسال الرسالة باستخدام التنسيق الصحيح: <message> @<username>'
            )

        # الرد بنتيجة الاستعلام
        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        _, username, message = data.split(':', 2)
        try:
            user = await client.get_entity(username)
            await event.answer(f"{message}", alert=True)
        except Exception as e:
            await event.answer(f'حدث خطأ: {str(e)}', alert=True)

client.run_until_disconnected()
