import requests, os, operator, asyncio, random, uuid, datetime
from telethon import TelegramClient, events, Button
from telethon.errors import BadRequestError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

# إنشاء الجلسة
ABH = TelegramClient("ubot", api_id, api_hash)
@ABH.on(events.NewMessage(pattern="الحساب$"))
async def count(event):
    """For .count command, get profile stats."""
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    catevent = await event.edit("᯽︙ يتم الحساب انتـظر ")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity):
            g += 1
        elif isinstance(currrent_entity):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1

    result += f"**᯽︙ الأشخاص:**\t**{u}**\n"
    result += f"**᯽︙ الـمجموعات:**\t**{g}**\n"
    result += f"**᯽︙ المجموعات الخارقه:**\t**{c}**\n"
    result += f"**᯽︙ القنوات:**\t**{bc}**\n"
    result += f"**᯽︙ البوتات:**\t**{b}**"

    await catevent.edit(result)
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
