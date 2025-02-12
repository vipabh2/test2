from telethon import TelegramClient, events
from telethon.tl.functions.messages import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import os

# جلب البيانات من متغيرات البيئة
api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل البوت
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if event.is_group:  # إذا كانت الرسالة في مجموعة
        # التحقق إذا كانت الرسالة تحتوي على أمر تقييد
        if event.raw_text.startswith('!تقييد'):
            # التأكد أن المرسل هو مشرف في المجموعة
            if event.sender_id in [admin.user_id for admin in await event.get_chat_admins()]:
                # استخراج معرف المستخدم من الرسالة
                try:
                    user_id = int(event.raw_text.split()[1])  # رقم معرف المستخدم
                    # تقييد المستخدم من إرسال الرسائل
                    await event.client(EditBannedRequest(event.chat_id, user_id, ChatBannedRights(
                        until_date=None,  # لا يوجد تاريخ محدد للتقييد
                        send_messages=True  # تقييد إرسال الرسائل
                    )))
                    await event.reply(f"✅ تم تقييد المستخدم {user_id} من إرسال الرسائل في هذه المجموعة!")
                except IndexError:
                    await event.reply("🚨 **خطأ:** يجب إدخال معرف المستخدم بعد الأمر.")
                except ValueError:
                    await event.reply("🚨 **خطأ:** يجب إدخال معرف المستخدم بشكل صحيح.")
                except Exception as e:
                    await event.reply(f"🚨 **خطأ:** حدث خطأ غير متوقع: {e}")
            else:
                await event.reply("🚨 **خطأ:** ليس لديك صلاحيات كافية لتقييد المستخدم!")
    
# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
