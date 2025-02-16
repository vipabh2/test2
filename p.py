import requests, os, operator, asyncio, random, uuid, datetime
from telethon import TelegramClient, events, Button
from telethon.errors import BadRequestError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

# إنشاء الجلسة
ABH = TelegramClient("ubot", api_id, api_hash)

@ABH.on(events.NewMessage(pattern="قنواتي$"))
async def _(event):
    "To list all public channels and groups."
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "᯽︙ جميع القنوات والمجموعات التي قمت بأنشائها :\n"
    output_str += "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await event.edit(output_str)

@ABH.on(events.NewMessage(pattern="الاحداث( -ر)?(?: |$)(\d*)?"))
async def iundlt(event):
    await event.edit("᯽︙ يـتم الـبحث عن اخـر الاحداث")
    flag = event.pattern_match.group(1)
    lim = int(event.pattern_match.group(2) or 5)
    
    if lim > 15:
        lim = 15
    if lim <= 0:
        lim = 1

    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )

    deleted_msg = f"᯽︙ اخـر {lim} رسـائل مـحذوفة فـي الـدردشة :"
    if not flag:
        for msg in adminlog:
            ruser = await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            msg_media_type = media_type(msg.old)
            if msg_media_type is None:
                deleted_msg += f"\n {msg.old.message} \n ᯽︙ تم ارسالها بـواسطة {ruser.users[0].first_name}"
            else:
                deleted_msg += f"\n {msg_media_type} \n ᯽︙ ارسلت بـواسطـة {ruser.users[0].first_name}"
        await event.edit(deleted_msg)
    else:
        main_msg = await event.reply(deleted_msg)
        for msg in adminlog:
            ruser = await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            msg_media_type = media_type(msg.old)
            if msg_media_type is None:
                await main_msg.edit(f"{msg.old.message}\n᯽︙ ارسلت بواسطه {ruser.users[0].first_name}")
            else:
                await main_msg.edit(f"{msg.old.message}\n᯽︙ ارسلت بواسطه {ruser.users[0].first_name}",
                                     file=msg.old.media)

# بدء الجلسة
ABH.start()
ABH.run_until_disconnected()
