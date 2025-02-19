import os, re
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

plugin_category = "extra"
@ABH.on(events.NewMessage(pattern=r"المحذوفين ?([\s\S]*)"))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**⎉╎لا توجـد حـسابات محذوفـة في هـذه المجموعـة !**"
    if con != "تنظيف":
        event = await event.edit(show, "**⎉╎جـارِ البحـث عـن الحسابـات المحذوفـة ⌯**")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**⎉╎تم ايجـاد  {del_u}  من  الحسابـات المحذوفـه في هـذه المجموعـه**\n**⎉╎لحذفهـم إستخـدم الأمـر  ⩥ :**  `.المحذوفين تنظيف`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.edit(show, "**⎉╎ليس لـدي صلاحيـات المشـرف هنـا ؟!**", 5)
        return
    event = await event.edit(show, "**⎉╎جـارِ حـذف الحسـابات المحذوفـة ⌯**")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await event.edit(event, "**⎉╎ ليس لدي صلاحيات الحظر هنا**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**⎉╎تـم حـذف  {del_u}  الحسـابات المحذوفـة ✓**"
    if del_a > 0:
        del_status = f"**⎉╎تـم حـذف {del_u} الحسـابات المحذوفـة، ولڪـن لـم يتـم حذف الحسـابات المحذوفـة للمشرفيـن !**"
    await event.edit(event, del_status, 5)

  
@ABH.on(events.NewMessage(pattern=".رسائلي$"))
async def zed(event):
    zzm = "me"
    a = await event.edit(event.chat_id, 0, from_user=zzm)
    await event.edit(event, f"**⎉╎لديـك هنـا ⇽**  `{a.total}`  **رسـالـه 📩**")


@ABH.on(events.NewMessage(pattern=".رسائله$"))
async def zed(event):
    k = await event.get_reply_message()
    if k:
        a = await event.edit(event.chat_id, 0, from_user=k.sender_id)
        return await event.edit(event, f"**⎉╎لديـه هنـا ⇽**  `{a.total}`  **رسـالـه 📩**")
    zzm = event.pattern_match.group(1)
    if zzm:
        a = await event.edit(event.chat_id, 0, from_user=zzm)
        return await event.edit(event, f"**⎉╎المستخـدم** {zzm} **لديـه هنـا ⇽**  `{a.total}`  **رسـالـه 📩**")
    else:
        await event.edit(event, f"**⎉╎بالـرد ع الشخص او بـ إضافة أيـدي او يـوزر الشخـص لـ الامـر**")


@ABH.on(events.NewMessage(pattern=".رسائل$"))
async def zed(event):
    k = await event.get_reply_message()
    if k:
        a = await event.edit(event.chat_id, 0, from_user=k.sender_id)
        return await event.edit(event, f"**⎉╎لديـه هنـا ⇽**  `{a.total}`  **رسـالـه 📩**")
    zzm = event.pattern_match.group(1)
    if zzm:
        a = await event.edit(event.chat_id, 0, from_user=zzm)
        return await event.edit(event, f"**⎉╎المستخـدم** {zzm} **لديـه هنـا ⇽**  `{a.total}`  **رسـالـه 📩**")
    else:
        await event.edit(event, f"**⎉╎بالـرد ع الشخص او بـ إضافة أيـدي او يـوزر الشخـص لـ الامـر**")
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

@ABH.on(events.NewMessage(pattern=".امسح$"))
async def delete_filtered_messages(event):
    if event.sender_id != 1910015590:
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
        # التعامل مع الأخطاء
        await event.reply(f"حدث خطأ أثناء الحذف: {str(e)}")
@ABH.on(events.NewMessage(pattern="امسح صور$"))
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
@ABH.on(events.NewMessage(pattern="مشاركاتة (الكل)?(?:\s|$)([\s\S]*)"))
async def fast_purger(event):
    "To purge messages from the replied message of replied user."
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if not reply or reply.sender_id is None:
        return await event.edit(
            event, "**- خطـأ :**\n__This cmd Works only if you reply to user message.__"
        )
    if not flag:
        if input_str and p_type == "كلمة":
            async for msg in event.client.iter_messages(
                event.chat_id,
                search=input_str,
                from_user=reply.sender_id,
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str and input_str.isnumeric():
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=int(input_str),
                offset_id=reply.id - 1,
                reverse=True,
                from_user=reply.sender_id,
            ):
                msgs.append(msg)
                count += 1
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            error += f"\n• `.upurge {input_str}` __is invalid syntax try again by reading__ `.help -c purge`"
        else:
            async for msg in event.client.iter_messages(
                chat,
                min_id=event.reply_to_msg_id - 1,
                from_user=reply.sender_id,
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(
            chat,
            limit=int(input_str),
            from_user=reply.sender_id,
        ):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    else:
        async for msg in event.client.iter_messages(
            chat,
            from_user=reply.sender_id,
        ):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "**- حـذف رسائلـه تم بنجـاح ✅**\n**- تم حـذف** " + str(count) + "**رسالـه 🗑**"
    if error != "":
        result += f"\n\n**- خطـأ :**{error}"
    if not result:
        result += "**- عـذراً .. الرسـالة غيـر موجـودة**"

# بدء الجلسة
ABH.start()
ABH.run_until_disconnected()
