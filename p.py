from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

async def get_user_from_event(mention):
    """استرجاع المستخدم بناءً على الرقم ID المرسل في الرسالة."""
    user_id = mention.text.split(' ')[1]  # استخراج رقم الـ ID من الرسالة بعد الفراغ
    try:
        # استرجاع كائن المستخدم باستخدام الـ ID
        user = await client.get_entity(user_id)
        return user, None  # لا يوجد نص مخصص في هذا الحال
    except Exception as e:
        return None, None  # في حال لم يتم العثور على المستخدم

async def edit_or_reply(mention, message):
    """الدالة للرد برسالة أو تعديلها."""
    await mention.reply(message)

@client.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return await mention.reply("لم يتم العثور على المستخدم.")
    
    # إذا كان هناك نص مخصص
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    
    # إذا لم يكن هناك نص مخصص، نعرض اسم المستخدم أو الاسم الأول
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙[{tag}](tg://user?id={user.id})")

client.start()
client.run_until_disconnected()
