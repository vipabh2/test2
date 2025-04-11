import os
import json
from telethon import TelegramClient, events
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
def load_data(filename="rose.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
def save_data(data, filename="rose.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
rose = load_data()
def add_user(uid, gid, name, rose, cost):
    uid, gid = str(uid), str(gid)
    if gid not in rose:
        rose[gid] = {}
    if uid not in rose[gid]:
        rose[gid][uid] = {
            "name": name,
            "money": 1201,
            "status": "عادي",
            "giver": None,
            "m": cost,
            "promote_value": 0
        }
    save_data(rose)
@ABH.on(events.NewMessage(pattern=r'ر(?:\s+(\d+))?'))
async def promote_handler(event):
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("يجب الرد على شخص حتى ترفعه.")
        return
    match = event.pattern_match
    cost = int(match.group(1)) if match.group(1) else 313
    giver_id = str(event.sender_id)
    receiver_id = str(message.sender_id)
    receiver_name = message.sender.first_name or "مجهول"
    giver_name = (await event.get_sender()).first_name or "مجهول"
    gid = str(event.chat_id)
    add_user(receiver_id, gid, receiver_name, rose, cost)
    add_user(giver_id, gid, giver_name, rose, cost)
    if rose[gid][receiver_id]["status"] == "مرفوع":
        await event.reply(f"{receiver_name} مرفوع من قبل.")
        return
    if cost < 1:
        await event.reply("🚫 أقل مبلغ مسموح للرفع هو 1.")
        return
    min_required = 10
    giver_money = rose[gid][giver_id]["money"]
    if giver_money < min_required:
        await event.reply(f"❌ رصيدك {giver_money}، والحد الأدنى للرفع هو {min_required}.")
        return
    if giver_money < cost:
        await event.reply(f"❌ رصيدك لا يكفي. تحاول ترفع بـ {cost} فلوس ورصيدك فقط {giver_money}.")
        return
    rose[gid][giver_id]["money"] -= cost
    rose[gid][receiver_id]["status"] = "مرفوع"
    rose[gid][receiver_id]["giver"] = giver_id
    rose[gid][receiver_id]["m"] = cost
    rose[gid][receiver_id]["promote_value"] = cost
    save_data(rose)
    await event.reply(f"🌹 تم رفع {receiver_name} مقابل {cost} فلوس.")
@ABH.on(events.NewMessage(pattern='ت'))
async def demote_handler(event):
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("متكدر تنزل العدم , سوي رد على شخص")
        return
    gid = str(event.chat_id)
    sender_id = str(event.sender_id)
    target_id = str(message.sender_id)
    target_name = message.sender.first_name or "مجهول"
    add_user(target_id, gid, target_name, rose, 0)
    add_user(sender_id, gid, event.sender.first_name, rose, 0)
    if rose[gid][target_id]["status"] != "مرفوع":
        await event.reply("المستخدم هاذ ما مرفوع من قبل😐")
        return
    giver_id = rose[gid][target_id].get("giver")
    executor_money = rose[gid][sender_id]["money"]
    promote_value = rose[gid][target_id].get("promote_value", 313)
    if sender_id == giver_id:
        cost = int(promote_value * 1.5)
    else:
        cost = int(promote_value * 2)
    if executor_money < cost:
        await event.reply(f"ما تگدر تنزله لأن رصيدك {executor_money}، والكلفة المطلوبة {cost}")
        return
    rose[gid][sender_id]["money"] -= cost
    rose[gid][target_id]["status"] = "عادي"
    rose[gid][target_id]["giver"] = None
    rose[gid][target_id]["promote_value"] = 0
    save_data(rose)
    await event.reply("تم تنزيل المستخدم من قائمة السمبات.")
@ABH.on(events.NewMessage(pattern='ا'))
async def show_handler(event):
    chat_id = str(event.chat_id)
    if chat_id not in rose or not rose[chat_id]:
        await event.reply("ماكو سمبات هنا بالمجموعة")
        return
    response = "قائمة الوردات👇\n"
    removed_users = []
    for uid in list(rose[chat_id].keys()):
        data = rose[chat_id][uid]
        if data.get("status") == "مرفوع":
            status_icon = "🌹"
            response += f"{status_icon} [{data['name']}](tg://user?id={uid}) ⇜ {data.get('promote_value', 0)}\n"
        else:
            removed_users.append(uid)
    for uid in removed_users:
        del rose[chat_id][uid]
    save_data(rose)
    await event.reply(response if response.strip() != "قائمة الوردات👇" else "ماكو وردات مرفوعين بالمجموعة", parse_mode="Markdown")
@ABH.on(events.NewMessage(pattern='ف'))
async def m(event):
    gid = str(event.chat_id)
    sender_id = str(event.sender_id)
    if gid not in rose or sender_id not in rose[gid]:
        name = (await event.get_sender()).first_name or "مجهول"
        add_user(sender_id, gid, name, rose, cost=0)
    m = rose[gid][sender_id]["money"]
    await event.reply(f'{m}')
ABH.run_until_disconnected()
