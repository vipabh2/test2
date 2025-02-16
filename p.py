import os
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

# إنشاء الجلسة
ABH = TelegramClient("ubot", api_id, api_hash)

from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl
)
plugin_category = "extra"

excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

@ABH.on(
    pattern="امسح(\s*| \d+)$", 
    command=("امسح", plugin_category),
    info={
        "header": "لحذف الرسائل من نوع معين.",
        "description": "يحذف الرسائل مثل الصور، الفيديوهات، الروابط، وغيرها بناءً على الفلاتر المحددة.",
        "usage": ["{tr}امسح"],
        "examples": "{tr}امسح",
    },
)
async def delete_filtered_messages(event):
    """حذف الرسائل بناءً على فلاتر محددة."""

    await event.delete() 

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الروابط": InputMessagesFilterUrl,
            "الصور": InputMessagesFilterPhotos
        }

        total_deleted = 0 
        deleted_counts = {key: 0 for key in filters.keys()}


        for msg_type, msg_filter in filters.items():
            async for message in event.client.iter_messages(event.chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue 
                if message:
                    await message.delete()
                    deleted_counts[msg_type] += 1
                    total_deleted += 1

        if total_deleted > 0:
            details = "\n".join([f"{msg_type}: {count}" for msg_type, count in deleted_counts.items() if count > 0])
            await event.reply(f"تم حذف {total_deleted} رسالة.\nالتفاصيل:\n{details}")
        else:
            await event.reply("لا توجد رسائل تطابق الفلاتر المحددة!")

    except Exception as e:
        # التعامل مع الأخطاء
        await event.reply(f"حدث خطأ أثناء الحذف: {str(e)}")
@ABH.ar_cmd(
    pattern="امسح صور(\s*| \d+)$", 
    command=("امسح", plugin_category),
    info={
        "header": "لحذف الرسائل من نوع معين.",
        "description": "يحذف الرسائل مثل الصور، الفيديوهات، الروابط، وغيرها بناءً على الفلاتر المحددة.",
        "usage": ["{tr}امسح"],
        "examples": "{tr}امسح",
    },
)
async def delete_filtered_messages(event):
    """حذف الرسائل بناءً على فلاتر محددة."""

    await event.delete() 

    try:
        filters = {
            "الصور": InputMessagesFilterPhotos
        }

        total_deleted = 0 
        deleted_counts = {key: 0 for key in filters.keys()}  


        for msg_type, msg_filter in filters.items():
            async for message in event.client.iter_messages(event.chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue 
                if message:
                    await message.delete()
                    deleted_counts[msg_type] += 1
                    total_deleted += 1

        if total_deleted > 0:
            details = "\n".join([f"{msg_type}: {count}" for msg_type, count in deleted_counts.items() if count > 0])
            await event.reply(f"تم حذف {total_deleted} رسالة.\nالتفاصيل:\n{details}")
        else:
            await event.reply("لا توجد رسائل تطابق الفلاتر المحددة!")

    except Exception as e:
        await event.reply(f"حدث خطأ أثناء الحذف: {str(e)}")

@ABH.on(events.NewMessage(pattern="قنواتي$"))
async def list_channels(event):
    """لإظهار جميع القنوات والمجموعات التي قمت بإنشائها."""
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "᯽︙ جميع القنوات والمجموعات التي قمت بأنشائها :\n"
    output_str += "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await event.edit(output_str)

@ABH.on(events.NewMessage(pattern="الاحداث( -ر)?(?: |$)(\d*)?"))
async def iundlt(event):
    """لإظهار الأحداث الأخيرة (الرسائل المحذوفة)"""
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
