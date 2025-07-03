from telethon.tl.functions.messages import SendReactionRequest
from telethon.sessions import StringSession
from telethon.tl.types import ReactionEmoji
from telethon import events, TelegramClient
import asyncio, json, re, os
def register_handlers(abh_dict):
    client = abh_dict["client"]

def input_session_data():
    sessions = []
    print("ملف sessions.json غير موجود. يرجى إدخال بيانات الجلسات:")
    while True:
        session_string = input("أدخل session_string (أو اتركه فارغًا للخروج): ").strip()
        if not session_string:
            break
        api_id = input("أدخل api_id (رقم صحيح): ").strip()
        api_hash = input("أدخل api_hash: ").strip()
        if not api_id.isdigit():
            print("خطأ: api_id يجب أن يكون رقمًا صحيحًا.")
            continue
        sessions.append({
            "session_string": session_string,
            "api_id": int(api_id),
            "api_hash": api_hash
        })
        print("تم إضافة جلسة. أدخل جلسة أخرى أو اترك الحقل فارغًا للخروج.")
    return sessions

def load_sessions(filename="sessions.json"):
    if not os.path.exists(filename):
        sessions = input_session_data()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)
        print(f"تم إنشاء {filename} وحفظ البيانات.")
        return sessions
    else:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"خطأ في قراءة JSON من الملف {filename}: {e}")
            return []

sessions_data = load_sessions()

ABHs = []
for sess in sessions_data:
    client = TelegramClient(StringSession(sess["session_string"]), sess["api_id"], sess["api_hash"])
    ABHs.append({
        "client": client,
        "target_user_id": None,
        "selected_emojis": []
    })    
@client.on(events.NewMessage(pattern=r'^ازعاج\s+(.+)$'))
async def set_target_user_with_reaction(event):
    global target_user_id, selected_emojis
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        target_user_id = reply_msg.sender_id
        emojis_str = event.pattern_match.group(1).strip()
        selected_emojis = [ReactionEmoji(emoticon=e.strip()) for e in emojis_str if e.strip()]
        await event.respond(f"\u2705 تم تفعيل نمط الإزعاج على المستخدم `{target_user_id}` باستخدام الرموز: {' '.join(e.emoticon for e in selected_emojis)}")
        print(f"تم تحديد {target_user_id} للتفاعل التلقائي باستخدام: {' '.join(e.emoticon for e in selected_emojis)}")
    else:
        await event.respond("\u2757 يجب الرد على رسالة المستخدم الذي تريد إزعاجه باستخدام الأمر: `ازعاج + \ud83c\udf53\ud83c\udf4c\u2728` (يمكنك وضع أكثر من رمز)")
@client.on(events.NewMessage(pattern=r'^الغاء ازعاج$'))
async def cancel_auto_react(event):
    global target_user_id, selected_emojis
    target_user_id = None
    selected_emojis = []
    await event.respond("\ud83d\udea9 تم إيقاف نمط الإزعاج. لن يتم التفاعل مع أي رسائل حالياً.")
    print("تم إلغاء نمط الإزعاج.")
@client.on(events.NewMessage())
async def auto_react(event):
    if target_user_id and event.sender_id == target_user_id and selected_emojis:
        try:
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=selected_emojis
            ))
            print(f"\u2705 تم التفاعل مع الرسالة {event.id} باستخدام الرموز: {' '.join(e.emoticon for e in selected_emojis)}")
        except Exception as e:
            print(f"\u26a0\ufe0f فشل التفاعل مع الرسالة {event.id}: {e}")
target_user_id = 1421907917
@client.on(events.NewMessage(pattern=r"^.كلمات (\d+)\s+(\d+)$", outgoing=True))
async def words(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    time = int(event.pattern_match.group(2)) or 1
    for i in range(num):
        async with client.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("كلمات")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\(\s*(.+?)\s*\)", text)
                    if match:
                        text = match.group(1)
                        await asyncio.sleep(time)
                        await conv.send_message(text)
                    break
            except asyncio.TimeoutError:
                return
@client.on(events.NewMessage(pattern=r"^.تركيب (\d+)$", outgoing=True))
async def unspilt(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for i in range(num):
        async with client.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("تركيب")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\(\s*(.+?)\s*\)", text)
                    if match:
                        text = match.group(1)
                        merged = ''.join(text.split())
                        await conv.send_message(merged)
                    break
            except asyncio.TimeoutError:
                return
@client.on(events.NewMessage(pattern=r"^.تفكيك (\d+)$", outgoing=True))
async def spilt(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for i in range(num):
        async with client.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("تفكيك")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\(\s*(.+?)\s*\)", text)
                    if match:
                        text = match.group(1)
                        clean = ''.join(text.split())
                        separated = ' '.join(clean)
                        await conv.send_message(separated)
                    break
            except asyncio.TimeoutError:
                return
@client.on(events.NewMessage(pattern=r"^.احسب (\d+)$", outgoing=True))
async def calc(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for _ in range(num):
        async with client.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("احسب")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"([\d\s\+\-\*÷\/\.]+)\s*=", text)
                    if match:
                        expression = match.group(1).replace('÷', '/').replace('×', '*').strip()
                        try:
                            result = eval(expression)
                            if isinstance(result, float) and result.is_integer():
                                result = int(result)
                            await conv.send_message(str(result))
                        except Exception:
                            await conv.send_message("خطأ في الحساب.")
                    break
            except asyncio.TimeoutError:
                return
@client.on(events.NewMessage(pattern=r"^.جمل (\d+)$", outgoing=True))
async def j(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for _ in range(num):
        async with client.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("جمل")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\((.*?)\)", text)
                    if match:
                        inside = match.group(1)
                        cleaned = re.sub(r"[↢⇜'«»]", "", inside)
                        normalized = re.sub(r"\s+", " ", cleaned).strip()
                        await conv.send_message(normalized)
                    else:
                        return
                    break
            except asyncio.TimeoutError:
                return
@client.on(events.NewMessage(pattern=r"^.تفاعل|تفاعل\s+(\d+)\s+(\d+(?:\.\d+)?)$", outgoing=True))
async def sends(event):
    much = int(event.pattern_match.group(1))
    time = float(event.pattern_match.group(2))
    r = await event.get_reply_message()
    if not r:
        await event.edit('🤔 يجب أن ترد على رسالة.')
        return
    for i in range(much):
        await words(event)
        await asyncio.sleep(time)
async def main():
    for abh_dict in ABHs:
        client = abh_dict["client"]

async def main():
    for abh_dict in ABHs:
        register_handlers(abh_dict)  # تسجيل الأحداث لكل جلسة
        await abh_dict["client"].start()
        print(f"تم تشغيل الجلسة: {abh_dict['client'].session.save()}")

    # تشغيل جميع الجلسات بشكل متزامن وانتظار انتهاءها
    await asyncio.gather(*[abh_dict["client"].run_until_disconnected() for abh_dict in ABHs])

if __name__ == "__main__":
    asyncio.run(main())
