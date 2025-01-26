from telethon import TelegramClient, events, Button
import os, random, asyncio

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
    
    await event.reply(f"عزيزي {n1} تم تسجيلك في لعبة فليبي.")
    await asyncio.sleep(3)
    
    await event.respond(
        f"عزيزي {n1} تم تسجيلك في لعبة فليبي.\nانتظر حتى يتم تسجيل اللاعب الآخر.",
        buttons=[[Button.inline("أنا", b"pl2")]]
    )

@ABH.on(events.CallbackQuery(data=b"pl2"))
async def pl2(event):
    global head, tail, p1, p2
    sender = await event.get_sender()
    p2 = event.sender_id
    n2 = sender.first_name
    
    head = random.choice([p1, p2])
    tail = p1 if head == p2 else p2
    n_h = (await ABH.get_entity(p1)).first_name
    n_t = (await ABH.get_entity(p2)).first_name
    await event.respond(f"عزيزي {n2} تم تسجيلك في لعبة فليبي.")
    await asyncio.sleep(3)
    await event.respond(f"اللاعب الأول هو {n_h} واللاعب الثاني هو {n_t}.")
    await asyncio.sleep(3)
    winner = random.choice([head, tail])
    await event.respond(f"الفائز هو {winner} 🎉")
ABH.run_until_disconnected()
