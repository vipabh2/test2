from telethon.tl.functions.messages import SendReactionRequest
from telethon.sessions import StringSession
from telethon.tl.types import ReactionEmoji
from telethon import events, TelegramClient
import asyncio, json, re
def load_sessions(filename="sessions.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
def save_sessions(sessions, filename="sessions.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)
sessions_data = load_sessions()
ABHs = []
for sess in sessions_data:
    ABH = TelegramClient(StringSession(sess["session_string"]), sess["api_id"], sess["api_hash"])
    ABHs.append({
        "ABH": ABH,
        "target_user_id": None,
        "selected_emojis": []
    })
async def start_ABH(ABH_dict):
    ABH = ABH_dict["ABH"]
    await ABH.start()
@ABH.on(events.NewMessage(pattern=r'^ازعاج\s+(.+)$'))
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
@ABH.on(events.NewMessage(pattern=r'^الغاء ازعاج$'))
async def cancel_auto_react(event):
    global target_user_id, selected_emojis
    target_user_id = None
    selected_emojis = []
    await event.respond("\ud83d\udea9 تم إيقاف نمط الإزعاج. لن يتم التفاعل مع أي رسائل حالياً.")
    print("تم إلغاء نمط الإزعاج.")
@ABH.on(events.NewMessage())
async def auto_react(event):
    if target_user_id and event.sender_id == target_user_id and selected_emojis:
        try:
            await ABH(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=selected_emojis
            ))
            print(f"\u2705 تم التفاعل مع الرسالة {event.id} باستخدام الرموز: {' '.join(e.emoticon for e in selected_emojis)}")
        except Exception as e:
            print(f"\u26a0\ufe0f فشل التفاعل مع الرسالة {event.id}: {e}")
target_user_id = 1421907917
@ABH.on(events.NewMessage(pattern=r"^.كلمات (\d+)\s+(\d+)$", outgoing=True))
async def words(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    time = int(event.pattern_match.group(2)) or 1
    for i in range(num):
        async with ABH.conversation(event.chat_id, timeout=10) as conv:
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
@ABH.on(events.NewMessage(pattern=r"^.تركيب (\d+)$", outgoing=True))
async def unspilt(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for i in range(num):
        async with ABH.conversation(event.chat_id, timeout=10) as conv:
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
@ABH.on(events.NewMessage(pattern=r"^.تفكيك (\d+)$", outgoing=True))
async def spilt(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for i in range(num):
        async with ABH.conversation(event.chat_id, timeout=10) as conv:
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
@ABH.on(events.NewMessage(pattern=r"^.احسب (\d+)$", outgoing=True))
async def calc(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for _ in range(num):
        async with ABH.conversation(event.chat_id, timeout=10) as conv:
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
@ABH.on(events.NewMessage(pattern=r"^.جمل (\d+)$", outgoing=True))
async def j(event):
    await event.delete()
    num = int(event.pattern_match.group(1)) or 1
    for _ in range(num):
        async with ABH.conversation(event.chat_id, timeout=10) as conv:
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
@ABH.on(events.NewMessage(pattern=r"^.تفاعل|تفاعل\s+(\d+)\s+(\d+(?:\.\d+)?)$", outgoing=True))
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
    print(f"تم تشغيل الجلسة: {ABH.session.save()[:20]}...")
    await ABH.run_until_disconnected()
async def main():
    await asyncio.gather(*(start_ABH(c) for c in ABHs))
if __name__ == "__main__":
    asyncio.run(main())
