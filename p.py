from telethon import TelegramClient, events
import os
import asyncio
from googletrans import Translator

# تحميل المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')

# بدء عميل التليجرام
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r'^(مخفي طكة زيج|زيج)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message and replied_message.sender_id == 1910015590:
        await event.reply("عزيزي الغبي ... \n تريدني اعفط للمطور شكلت لربك؟")
        return
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/VIPABH/1171", reply_to=replied_message.id)
    else:
        await event.reply("عزيزي الفاهي ... \n الامر يعمل بالرد , اذا عدتها وما سويت رد اعفطلك")
ABH.run_until_disconnected()
