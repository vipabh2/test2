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
            "money": 1200,
            "status": "عادي",
            "giver": None,
            "cost": cost
        }
    save_data(rose)
@ABH.on(events.NewMessage(pattern=r'رفع وردة(?:\s+(\d+))?'))
async def promote_handler(event):
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("الامر يعمل بالرد , تحب اسويلك شرح🙄؟")
        return
    giver_id = str(event.sender_id)
    receiver_id = str(message.sender_id)
    receiver_name = message.sender.first_name or "مجهول"
    gid = str(event.chat_id)
    add_user(receiver_id, gid, receiver_name, rose)
    add_user(giver_id, gid, event.sender.first_name, rose)
    if rose[gid][receiver_id]["status"] == "مرفوع":
        await event.reply(f"{receiver_name} مرفوع من قبل")
        return
    match = event.pattern_match
    try:
        cost = int(match.group(1)) if match.group(1) else 2
    except ValueError:
        return
    x = 1
    if cost < x:
        await event.reply(f"اقل مبلغ تكدر ترفع بي {x}")
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
    rose[gid][receiver_id]["cost"] = cost
    save_data(rose)
    await event.reply(f"🌹 تم رفع {receiver_name} مقابل {cost} فلوس.")
@ABH.on(events.NewMessage(pattern=r'تنزيل وردة'))
async def demote_handler(event):
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("متكدر تنزل العدم , سوي رد على شخص")
        return
    executor_id = str(event.sender_id)
    target_id = str(message.sender_id)
    target_name = message.sender.first_name or "مجهول"
    gid = str(event.chat_id)
    add_user(target_id, gid, target_name, rose)
    add_user(executor_id, gid, event.sender.first_name, rose)
    if rose[gid][target_id]["status"] != "مرفوع":
        await event.reply("المستخدم هاذ ما مرفوع من قبل😐")
        return
    giver_id = rose[gid][target_id].get("giver")
    if executor_id == target_id or executor_id == giver_id:
        cost = 2
    else:
        cost = 4
    min_required = 3000
    executor_money = rose[gid][executor_id]["money"]
    if executor_money < min_required:
        await event.reply(f"ماتكدر تنزله لان رصيدك {executor_money} لازم يكون {min_required} ")
        return
    rose[gid][executor_id]["money"] -= cost
    rose[gid][target_id]["status"] = "عادي"
    rose[gid][target_id]["giver"] = None
    save_data(rose)
    await event.reply(f"تم تنزيل المستخدم من قائمة الوردات")
@ABH.on(events.NewMessage(pattern='الحساب'))
async def show_handler(event):
    chat_id = str(event.chat_id)
    if chat_id not in rose or not rose[chat_id]:
        await event.reply("ماكو وردات هنا بالمجموعة!")
        return
    response = "قائمة الوردات👇\n"
    for uid, data in rose[chat_id].items():
        status_icon = "🌹" if data.get("status") == "مرفوع" else "👤"
        response += f"{status_icon} [{data['name']}](tg://user?id={uid}) ب سعر {data['cost']}\n"
    await event.reply(response, parse_mode="Markdown")
ABH.run_until_disconnected()
