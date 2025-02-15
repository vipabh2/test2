import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights

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
    # التحقق إذا كان المستخدم قد تم تقييده
    if event.action == 'user_banned' and event.user_id:
        print(f"تم تقييد المستخدم {event.user_id} بواسطة بوت أو مشرف آخر.")
        
        # التحقق إذا كانت الصلاحيات الحالية تساوي القيود
        current_permissions = await client.get_permissions(event.chat_id, event.user_id)
        
        # إذا كانت الصلاحيات تساوي القيود المحددة
        if current_permissions == restrict_rights:
            print(f"صلاحيات المستخدم {event.user_id} هي نفس القيود المحددة.")
            
            # الانتظار لمدة ثانية واحدة
            await asyncio.sleep(1)
            
            # إلغاء تقييد المستخدم بعد ثانية
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
