import requests, os, operator, asyncio, random, uuid, datetime 
from telethon import TelegramClient, events, Button
from telethon.errors import BadRequestError
from telethon.tl.functions.users import GetFullUserRequest


api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  

# إنشاء الجلسة
client = TelegramClient("userbot", api_id, api_hash)

@ABH.on(events.NewMessage(pattern="الاحداث( -ر)?(?: |$)(\d*)?"))
async def iundlt(event):
    uid = event.sender_id
    await event.reply(event, "᯽︙ يـتم الـبحث عن اخـر الاحداث")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"᯽︙ اخـر {lim} رسـائل مـحذوفة فـي الـدردشة :"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).users[0]
            media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n {msg.old.message} \n ᯽︙ تم ارسالها بـواسطة {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n {_media_type} \n ᯽︙ ارسلت بـواسطـة {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await event.reply(uid, deleted_msg)
    else:
        main_msg = await event.reply(uid, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).users[0]
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n᯽︙ ارسلت بواسطه {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n᯽︙ ارسلت بواسطه {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )


ABH.run_until_disconnected()
