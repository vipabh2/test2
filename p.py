from telethon import TelegramClient, events
from playwright.async_api import async_playwright
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
async def take_screenshot(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)
            screenshot_path = "screenshot.png"
            await page.screenshot(path=screenshot_path)
        except Exception as e:
            print(f"❌ خطأ أثناء تحميل الصفحة: {e}")
            screenshot_path = None
        finally:
            await browser.close()
    return screenshot_path
@ABH.on(events.NewMessage(pattern='سكرين|دز (.+)'))
async def handler(event):
    url = event.pattern_match.group(1)
    screenshot_path = await take_screenshot(url)
    if screenshot_path:
        await event.reply('تم التقاط لقطة الشاشة:', file=screenshot_path)
    else:
        await event.reply("هنالك خطأ في الرابط او الموقع \n دز شيء اخر")
print("✅ البوت يعمل... انتظر الأوامر!")
ABH.run_until_disconnected()
