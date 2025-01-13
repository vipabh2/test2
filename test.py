import re
from telethon import TelegramClient, events
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText
from database import save_message  

api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    query = event.text
    pattern = r"(.+?) @([\w\d_]+)"
    match = re.match(pattern, query)

    if match:
        message_text = match.group(1).strip()
        target_user = match.group(2)

        save_message(message_text, target_user)  # حفظ الرسالة في قاعدة البيانات

        result = [
            InputBotInlineResult(
                id="1",
                type="article",
                title=f"إرسال همسة إلى @{target_user}",
                description=f"النص الذي سيتم إرساله: {message_text}",
                # send_message=InputBotInlineMessageText(
                    message=f"تم إرسال الهمسة:\n{message_text}\nإلى @{target_user}. اضغط لتأكيد الإرسال."
                )
            )
        ]
    else:
        result = [
            InputBotInlineResult(
                id="1",
                type="article",
                title="صيغة غير صحيحة",
                description="يرجى إدخال صيغة صحيحة (النص + @اليوزر).",
                send_message=InputBotInlineMessageText(
                    message="يرجى استخدام الصيغة الصحيحة: النص + @اليوزر."
                )
            )
        ]

    await event.answer(result, cache_time=0)

print("البوت يعمل الآن...")
client.run_until_disconnected()
