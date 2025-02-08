from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.ChatMemberUpdated)
async def handler(event):
    # عندما ينضم عضو جديد
    if event.new_user:
        print(f"عضو جديد انضم: {event.new_user.id}")
    
    # عندما يغادر عضو
    if event.left:
        print(f"عضو غادر: {event.old_user.id}")
    
    # التحقق من التغييرات في صلاحيات الأعضاء
    if event.new_admin:
        print(f"تم تعيين عضو كمسؤول: {event.new_user.id}")
    elif event.old_admin and not event.new_admin:
        print(f"تم سحب صلاحيات المسؤول عن العضو: {event.old_user.id}")

client.start()
client.run_until_disconnected()
