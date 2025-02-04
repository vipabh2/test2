import os
from telethon import TelegramClient, events

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r"^ارسل\s+(.+?)\s+(@\w+)$"))
async def send_message_to_user(event):
    message = event.pattern_match.group(1)
    username = event.pattern_match.group(2)
    receiver = await ABH.get_entity(username)
    receiver_id = receiver.id
    sender_id = event.sender_id
    await ABH.send_message(
        receiver_id,
        f"اكو فد واحد دزلك رسالة بس شخصيتة ضعيفة دزها مخفية \n الرسالة 👇 \n {message}"
    )
    await ABH.send_message(
        sender_id,
        f"رسالتك الفارغة دزيتها, مرة لخ دزها انت وصير سبع \n دزيتها ل {username}"
    )

print("✅ Bot is running...")
ABH.run_until_disconnected()
