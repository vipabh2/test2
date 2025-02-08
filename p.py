from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time, os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
client = TelegramClient("session_name", api_id, api_hash)
# تشغيل Telethon كبوت
client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

async def take_screenshot():
    """وظيفة تأخذ لقطة شاشة للموقع باستخدام Selenium."""
    service = Service("C:/path/to/chromedriver.exe")  # ضع مسار ChromeDriver الصحيح
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=service, options=options)

    # فتح الموقع المطلوب
    driver.get("https://github.com/VIPABH")

    # انتظار تحميل الصفحة بالكامل
    time.sleep(3)

    # التقاط لقطة شاشة وحفظها
    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)

    # إغلاق المتصفح
    driver.quit()

    return screenshot_path

# حدث عند استقبال رسالة تحتوي على "دز"
@client.on(events.NewMessage(pattern="(?i)^دز$"))
async def handler(event):
    """عند إرسال كلمة 'دز' يقوم البوت بأخذ لقطة شاشة وإرسالها."""
    await event.reply("⏳ جاري التقاط لقطة الشاشة...")

    # التقاط لقطة الشاشة
    screenshot_path = await take_screenshot()

    # إرسال الصورة
    await client.send_file(event.chat_id, screenshot_path, caption="📸 لقطة الشاشة المطلوبة!")

# تشغيل البوت
print("✅ البوت يعمل... انتظر الأوامر!")
client.run_until_disconnected()

