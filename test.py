import re
from telethon import TelegramClient, events, Button

# إعدادات البوت
api_id = "20464188"  # ضع معرف API الخاص بك
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"  # ضع API Hash الخاص بك
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"  # ضع توكن البوت الخاص بك

# إنشاء جلسة البوت
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    query = event.text
    pattern = r"(.+?) @([\w\d_]+)"  # نمط لاستخراج النص واسم المستخدم الهدف
    match = re.match(pattern, query)

    if match:
        message_text = match.group(1).strip()  # النص المستهدف
        target_user = match.group(2)  # اسم المستخدم الهدف بدون @

        # إنشاء النتيجة المرسلة في الوضع Inline مع زر
        result = [
            InputBotInlineResult(
                id="1",
                type="article",
                title=f"إرسال همسة إلى @{target_user}",
                description=f"اضغط لعرض الهمسة إلى @{target_user}",
                send_message=InputBotInlineMessageText(
                    message="💌 اضغط على الزر أدناه لعرض الهمسة الخاصة.",
                    buttons=[
                        [Button.inline("👀 عرض الهمسة", data=f"{message_text}")]
                    ]
                )
            )
        ]
    else:
        # إذا كانت الصيغة غير صحيحة
        result = [
            InputBotInlineResult(
                id="1",
                type="article",
                title="صيغة غير صحيحة",
                description="يرجى إدخال صيغة صحيحة (النص + @اليوزر).",
                send_message=InputBotInlineMessageText(
                    message="⚠️ يرجى استخدام الصيغة الصحيحة:\n\nالنص + @اسم_المستخدم."
                )
            )
        ]

    # إرسال النتيجة
    await event.answer(result, cache_time=0)

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    # معالجة الزر عند الضغط عليه
    message_text = event.data.decode("utf-8")  # قراءة النص من الزر
    await event.edit(f"💌 الهمسة الخاصة:\n\n{message_text}")

# تشغيل البوت
print("💡 البوت يعمل الآن...")
client.run_until_disconnected()
