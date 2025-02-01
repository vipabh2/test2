from telethon import TelegramClient
from telethon import events, Button
import asyncio, os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

head = None
tail = None
p1 = None
p2 = None

@ABH.on(events.NewMessage(pattern='/fliby'))
async def fliby(event):
    global head, tail, p1, p2
    sender = await event.get_sender()
    p1 = event.sender_id
    n1 = sender.first_name
    await event.reply(f"عزيزي {n1} جاري تسجيلك في لعبة فليبي.",
                      buttons=[[Button.inline("صورة", b"pic"), Button.inline("كتابة", b"text")]]
                      )
    await asyncio.sleep(3)
    await event.respond(f"عزيزي {n1} تم تسجيلك في لعبة فليبي.\nانتظر حتى يتم تسجيل اللاعب الآخر.")

@ABH.on(events.CallbackQuery(data=b"pic"))
async def pic(event):
    global p1, p2
    p2 = event.sender_id
    if p1 == p2:
        await event.respond("لا يمكنك اللعب مع نفسك.", alert=True)
        return
    if not p1 or not p2:
        await event.respond("لا يوجد لاعب غيرك", alert=True)
        return

ABH.run_until_disconnected()
