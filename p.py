from telethon import TelegramClient, events
import os

# الحصول على المتغيرات من البيئة
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@client.on(events.NewMessage(pattern='^رفع مطور$'))
async def promote_dev(event):
    user_id = event.sender_id
    if user_id == 1910015590:
        await event.respond("عزيزي ابن هاشم مخفي، أنت ما متحملك فوكاها مطور آخر؟")
    else:
        await event.respond("دروح بابه روح، الأمر هذا للمطورين فقط")
@client.on(events.NewMessage(pattern='^رفع سمب$'))
async def promote_simp(event):
    user_id = event.sender_id
    sender_name = event.sender.first_name
    repmsg = await event.get_reply_message()
    target_user = await repmsg.get_sender() 
    target_name = target_user.first_name
    if target_user.id == 1910015590:
        await event.respond(f"ها ابن هاشم سالمين؟؟")
    else:
        await event.respond(f"لعيونك تم رفع {target_name} سمب\n جا قابل المطور سمب؟ 😂")

client.run_until_disconnected()
