import os
from telethon import TelegramClient, events
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl
)

# استبدل بـ API_ID و API_HASH الخاصة بك
api_id = os.getenv('API_ID')  # API_ID من تطبيق Telegram الخاص بك
api_hash = os.getenv('API_HASH')  # API_HASH من تطبيق Telegram الخاص بك

# أنشئ العميل باستخدام TelegramClient
client = TelegramClient('session_name', api_id, api_hash)

plugin_category = "extra"
excluded_user_ids = {793977288, 1421907917, 7308514832, 6387632922, 7908156943}

@client.on(events.NewMessage(pattern=r"\.رسائلي$"))
async def my_messages(event):
    count = await event.client.get_messages(event.chat_id, from_user="me", limit=0)
    await event.edit(f"**⎉╎لديـك هنـا ⇽** `{count.total}` **رسـالـه 📩**")

@client.on(events.NewMessage(pattern=r"\.رسائل(?:ه)?(?:\s+(.+))?$"))
async def user_messages(event):
    user = await event.get_reply_message() or event.pattern_match.group(1)
    if not user:
        return await event.edit("**⎉╎بالـرد ع الشخص او بـ إضافة أيـدي او يـوزر الشخـص لـ الامـر**")

    try:
        user_id = user.sender_id if hasattr(user, 'sender_id') else (await event.client.get_entity(user)).id
    except:
        return await event.edit("**⎉╎تعذّر العثـور علـى المستخـدم 🚫**")

    if user_id in excluded_user_ids:
        return await event.edit("**⎉╎لا يمكـن عرض رسـائـل هـذا المستخـدم 🚫**")

    count = await event.client.get_messages(event.chat_id, from_user=user_id, limit=0)
    await event.edit(f"**⎉╎لديـه هنـا ⇽** `{count.total}` **رسـالـه 📩**")

ids = [201728276, 7864847751, 1910015590]

@client.on(events.NewMessage(pattern="/امسح$"))
async def delete_filtered_messages(event):
    if event.sender_id not in ids:
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

# لا تقم بإغلاق الجلسة بعد تنفيذ main()، استخدم هذه الطريقة لترك السكربت يعمل بلا انقطاع.
client.run_until_disconnected()
