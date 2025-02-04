import os
from telethon import TelegramClient, events
from telethon.errors import UsernameInvalidError, UsernameNotOccupiedError, PeerIdInvalidError

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r"^ارسل\s+(.+?)\s+(@\w+)$"))
async def send_message_to_user(event):
    message = event.pattern_match.group(1)
    username = event.pattern_match.group(2)
    sender_id = event.sender_id
    
    try:
        receiver = await ABH.get_entity(username)
        receiver_id = receiver.id
        
        await ABH.send_message(
            receiver_id,
            f"اكو فد واحد دزلك رسالة بس شخصيتة ضعيفة دزها مخفية \n الرسالة 👇 \n {message}"
        )
        await ABH.send_message(
            sender_id,
            f"رسالتك وصلت بنجاح إلى {username}."
        )
    
    except (UsernameInvalidError, UsernameNotOccupiedError, PeerIdInvalidError):
        await ABH.send_message(sender_id, "❌ اليوزرنيم اللي دخلته غير صحيح أو الحساب خاص وما أكدر أوصله.")
    except Exception as e:
        await ABH.send_message(sender_id, f"❌ صار خطأ غير متوقع: {str(e)}")

print("\u2705 Bot is running...")
ABH.run_until_disconnected()
