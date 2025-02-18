import os, re
from telethon import TelegramClient, events
from PIL import Image
import io
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

# إنشاء الجلسة
ABH = TelegramClient("ubot", api_id, api_hash)



# دالة لتحويل الصورة إلى GIF
def convert_to_gif(image_path):
    image = Image.open(image_path)
    gif_path = "converted_image.gif"
    image.save(gif_path, format="GIF")
    return gif_path

# التعامل مع الصور الواردة
@ABH.on(events.NewMessage)
async def handler(event):
    if event.photo:
        # حفظ الصورة مؤقتاً
        photo = await event.download_media(file="temp_image.jpg")
        
        # تحويل الصورة إلى GIF
        gif_path = convert_to_gif("temp_image.jpg")
        
        # إرسال الصورة المحولة إلى GIF
        await event.reply(file=gif_path)

# تشغيل البوت
ABH.start()
ABH.run_until_disconnected()


