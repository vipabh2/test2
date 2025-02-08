from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# معلومات Telethon - استبدلها بمعلوماتك
api_id = 1234567  # ضع API ID الخاص بك
api_hash = "your_api_hash"  # ضع API Hash الخاص بك
bot_token = "your_bot_token"  # ضع توكن البوت

# تشغيل Telethon كبوت
client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# وظيفة Selenium لأخذ لقطة شاشة
async def take_screenshot():
    """وظيفة تأخذ لقطة شاشة للموقع باستخدام Selenium على Linux."""
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # إنشاء WebDriver مع تحديد مسار ChromeDriver
    service = Service("/usr/local/bin/chromedriver")  # تأكد من أن ChromeDriver في المسار الصحيح
    driver = webdriver.Chrome(service=service, options=options)

    # فتح الموقع المطلوب
    driver.get("https://github.com/VIPABH")

    # الانتظار حتى يتم تحميل الصفحة بالكامل
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))  # يمكنك تعديل هذا للبحث عن عنصر معين
        )
    except Exception as e:
        print(f"خطأ في تحميل الصفحة: {e}")
        driver.quit()
        return None

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

    # إرسال الصورة إلى نفس المحادثة
    if screenshot_path:
        await client.send_file(event.chat_id, screenshot_path, caption="📸 لقطة الشاشة المطلوبة!")

# تشغيل البوت
print("✅ البوت يعمل... انتظر الأوامر!")
client.run_until_disconnected()
