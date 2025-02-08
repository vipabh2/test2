from telethon import TelegramClient, events
from telethon.tl.types import ChatAdminRights
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.ChatAction)
async def handler(event):
    if event.user_added:
        print(f"عضو جديد انضم: {event.user_id}")
    
    if event.user_left:
        print(f"عضو غادر: {event.user_id}")
    
    if event.user_banned:
        print(f"تم حظر عضو: {event.user_id}")
    
    if event.user_unbanned:
        print(f"تم رفع الحظر عن عضو: {event.user_id}")
    
    # عندما يتم تغيير صلاحيات الأعضاء
    if event.admin_rights:
        rights = event.admin_rights
        if rights.add_admins:
            print(f"تم تعيين عضو كمسؤول: {event.user_id}")
        if rights.change_info:
            print(f"تم منح صلاحية تعديل معلومات المجموعة: {event.user_id}")
        if rights.invite_to_chat:
            print(f"تم منح صلاحية دعوة أعضاء جدد: {event.user_id}")
        if rights.ban_users:
            print(f"تم منح صلاحية حظر الأعضاء: {event.user_id}")

client.start()
client.run_until_disconnected()
