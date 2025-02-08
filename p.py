from telethon import TelegramClient, events
from playwright.async_api import async_playwright
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
BANNED_SITES = ["porn", "xvideos", "xnxx", "redtube", "xhamster", "brazzers", "youjizz", "spankbang", "erotic", "sex"]
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
def is_safe_url(url):
    return not any(banned in url.lower() for banned in BANNED_SITES)
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
@client.on(events.NewMessage(pattern='/دز (.+)'))
async def handler(event):
    url = event.pattern_match.group(1)
    if not is_safe_url(url):
        await event.reply("هذا الموقع محظور جرب تتواصل وي المطور @k_4x1")
        return
    screenshot_path = await take_screenshot(url)
    if screenshot_path:
        await event.reply('تم التقاط لقطة الشاشة:', file=screenshot_path)
    else:
        await event.reply("هنالك خطأ معين \n غير قادر علئ التقاط صوره")
client.run_until_disconnected()
