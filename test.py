import re
from telethon import TelegramClient, events
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText

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

        # إنشاء النتيجة المرسلة في الوضع Inline
        result = [
            InputBotInlineResult(
                id="1",
                type="article",
                title=f"إرسال همسة إلى @{target_user}",
                description=f"النص الذي سيتم إرساله: {message_text}",
                send_message=InputBotInlineMessageText(
                    message=f"⚡ تم إرسال همسة خاصة:\n\n💌 {message_text}\n\n👤 إلى: @{target_user}."
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

# تشغيل البوت
print("💡 البوت يعمل الآن...")
client.run_until_disconnected()
