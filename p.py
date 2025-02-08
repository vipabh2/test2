from telethon import TelegramClient, events
from playwright.sync_api import sync_playwright
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
client = TelegramClient("session_name", api_id, api_hash)
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# وظيفة لالتقاط لقطة شاشة باستخدام Playwright
async def take_screenshot(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # تشغيل بدون واجهة رسومية
        page = browser.new_page()

        # فتح الرابط
        page.goto(url)

        # التقاط لقطة شاشة
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path)

        # إغلاق المتصفح
        browser.close()

    return screenshot_path

# التعامل مع الرسائل
@client.on(events.NewMessage(pattern='/دز (.+)'))
async def handler(event):
    url = event.pattern_match.group(1)  # استخراج الرابط من الرسالة
    screenshot_path = await take_screenshot(url)

    # إرسال الصورة للمستخدم
    await event.reply('تم التقاط لقطة الشاشة:', file=screenshot_path)

# تشغيل البوت
print("✅ البوت يعمل... انتظر الأوامر!")
client.run_until_disconnected()
