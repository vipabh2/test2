import asyncio, os
from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights

# تحميل API_ID و API_HASH و BOT_TOKEN من البيئة
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')

# إعداد عميل Telethon
client = TelegramClient('session_name', api_id, api_hash)

# تحديد القيود (الصلاحيات المحظورة)
restrict_rights = ChatBannedRights(
    until_date=None,
    send_messages=True, 
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

@client.on(events.ChatAction)
async def handler(event):
    # التحقق من نوع الحدث إذا كان تقييد المستخدم
    if isinstance(event.action, events.ChatAction.UserBanned):
        # التحقق إذا كان هناك user_id
        if event.user_id:
            print(f"تم تقييد المستخدم {event.user_id} بواسطة بوت أو مشرف آخر.")
            
            # الحصول على الصلاحيات الحالية للمستخدم في الدردشة
            current_permissions = await client.get_permissions(event.chat_id, event.user_id)
            
            # التحقق إذا كانت الصلاحيات الحالية تساوي القيود المحددة
            if current_permissions.send_messages == restrict_rights.send_messages and \
               current_permissions.send_media == restrict_rights.send_media and \
               current_permissions.send_stickers == restrict_rights.send_stickers and \
               current_permissions.send_gifs == restrict_rights.send_gifs and \
               current_permissions.send_games == restrict_rights.send_games and \
               current_permissions.send_inline == restrict_rights.send_inline and \
               current_permissions.embed_links == restrict_rights.embed_links:
                
                print(f"صلاحيات المستخدم {event.user_id} هي نفس القيود المحددة.")
                
                # الانتظار لمدة ثانية واحدة
                await asyncio.sleep(1)
                
                # إلغاء تقييد المستخدم بعد ثانية واحدة
                unrestrict_rights = ChatBannedRights(
                    until_date=None,
                    send_messages=True,  # السماح بإرسال الرسائل
                    send_media=True,     # السماح بإرسال الوسائط
                    send_stickers=True,  # السماح بإرسال الملصقات
                    send_gifs=True,      # السماح بإرسال الرسوم المتحركة
                    send_games=True,     # السماح بإرسال الألعاب
                    send_inline=True,    # السماح باستخدام الرسائل التفاعلية
                    embed_links=True     # السماح بإرسال الروابط
                )
                
                # إعادة صلاحيات المستخدم بعد ثانية واحدة
                await client.edit_permissions(event.chat_id, event.user_id, unrestrict_rights)
                print(f"تم إلغاء تقييد المستخدم {event.user_id}.")

client.start()
client.run_until_disconnected()
