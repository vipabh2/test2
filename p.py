from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from telethon.errors.rpcerrorlist import UserIdInvalidError, UserAdminInvalidError
import os
import time

async def extract_time(cat, time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d", "w")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await cat.edit("الوقت الذي تم تحديده غير صحيح")
            return None
        if unit == "s":
            bantime = int(time.time() + int(time_num) * 1)
        elif unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        elif unit == "w":
            bantime = int(time.time() + int(time_num) * 7 * 24 * 60 * 60)
        else:
            await cat.edit(
                f"خطأ في تحديد الوقت. اكتب من الأسفل:\n s, m, h, d, أو w: {time_val[-1]}"
            )
            return None
        return bantime
    await cat.edit(
        f"خطأ في تحديد الوقت. اكتب من الأسفل:\n s, m, h, d, أو w: {time_val[-1]}"
    )
    return None

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

joker_t8ed = "https://forkgraph.zaid.pro/file/ya744KD7Km3q"
joker_unt8ed = "https://forkgraph.zaid.pro/file/YMTcYN1GaXQy"

@ABH.on(
    events.NewMessage(pattern="تقييد_مؤقت(?:\s|$)([\s\S]*)")
)
async def tmuter(event):
    # التحقق من أن الأمر تم إرساله في مجموعة
    if not event.is_group:
        return await event.edit("⚠️ هذا الأمر يعمل فقط في المجموعات.")
    # الحصول على المستخدم الذي تم الرد عليه
    replied_message = await event.get_reply_message()
    if not replied_message:
        return await event.edit("⚠️ يرجى الرد على رسالة المستخدم الذي تريد تقييده.")

    user = replied_message.sender_id
    if not user:
        return await event.edit("❌ لم أتمكن من العثور على المستخدم.")

    # استخراج الوقت والسبب
    reason = event.pattern_match.group(1).strip() if event.pattern_match.group(1) else None
    if not reason:
        return await event.edit("᯽︙ انـت لم تقـم بـوضـع وقـت مع الامـر")

    reason_parts = reason.split(" ", 1)
    cattime = reason_parts[0].strip()
    reason = reason_parts[1].strip() if len(reason_parts) > 1 else None

    # استخراج الوقت
    ctime = await extract_time(event, cattime)
    if not ctime:
        return

    # التحقق من أن المستخدم لا يحاول تقييد نفسه
    if user == (await event.client.get_me()).id:
        return await event.edit("᯽︙ عـذرا لا يمـكننـي حـظر نفـسي")

    try:
        # تنفيذ التقييد
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )

        # إرسال رسالة التأكيد
        caption = (
            f"᯽︙ تم تقييد المستخدم {replied_message.sender.first_name} "
            f"[@{replied_message.sender.username or 'N/A'}] بنجاح ✅\n"
            f"᯽︙ السبب: {reason}\n" if reason else ""
            f"** ᯽︙ مدة التقييد: **`{cattime}`"
        )
        await event.client.send_file(
            event.chat_id,
            joker_t8ed,
            caption=caption,
        )

    except UserIdInvalidError:
        return await event.edit("**يبدو ان كتم الشخص تم الغائه**")
    except UserAdminInvalidError:
        return await event.edit(
            "** يبـدو أنك لسـت مشرف في المجموعة او تحاول كتم مشـرف هنا**"
        )
    except Exception as e:
        return await event.edit(f"`{str(e)}`")

# بدء تشغيل البوت

async def cancel_t8ed(event):
    await event.delete()
    user, _ = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await event.client.send_message(event.chat_id, "عذرًا، لا يمكنك إلغاء تقييد نفسك.")
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=None, send_messages=False),
            )
        )
        await event.client.send_file(
            event.chat_id,
            joker_unt8ed,
            caption=f"**᯽︙ تم الغاء تقييد المستخدم {_format.mentionuser(user.first_name, user.id)} بنجاح ✅.**"
        )
    except UserIdInvalidError:
        return await event.client.send_message(event.chat_id, "يبدو أن التقييد على هذا المستخدم تم إلغاؤه بالفعل.")
    except UserAdminInvalidError:
        return await event.client.send_message(event.chat_id, "يبدو أنك لست مشرفًا في المجموعة أو تحاول إلغاء تقييد مشرف هنا.")
    except Exception as e:
        return await event.client.send_message(event.chat_id, f"`{str(e)}`")
ABH.run_until_disconnected()
