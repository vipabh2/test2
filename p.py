import os
from asyncio import sleep
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl
)

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

# إنشاء الجلسة
ABH = TelegramClient("ubot", api_id, api_hash)
ids = [201728276, 7864847751, 1910015590]
@ABH.on(events.NewMessage(pattern="/امسح$"))
async def delete_filtered_messages(event):
    if event.sender_id not in ids:  # هنا تم إصلاح المشكلة واستبدال `uid` بـ `event.sender_id`
        await event.delete()
        return

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
        await event.reply(f"حدث خطأ أثناء الحذف: {str(e)}")

ABH.run_until_disconnected()
