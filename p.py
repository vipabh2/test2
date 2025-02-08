from telethon import TelegramClient, events
from playwright.async_api import async_playwright  # type: ignore
import os
import asyncio
from googletrans import Translator

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')

BANNED_SITES = [
    "porn", "xvideos", "xnxx", "redtube", "xhamster",
    "brazzers", "youjizz", "spankbang", "erotic", "sex"
]

DEVICES = {
    "pc": {"width": 1920, "height": 1080, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    "android": "Galaxy S5"
}

ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def is_safe_url(url):
    return not any(banned in url.lower() for banned in BANNED_SITES)

async def take_screenshot(url, device="pc"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        if device in DEVICES:
            if isinstance(DEVICES[device], str):
                device_preset = p.devices[DEVICES[device]]
                context = await browser.new_context(**device_preset)
            else:
                context = await browser.new_context(
                    user_agent=DEVICES[device]["user_agent"],
                    viewport={"width": DEVICES[device]["width"], "height": DEVICES[device]["height"]}
                )
            page = await context.new_page()
        else:
            page = await browser.new_page()

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)  # تأخير 3 ثواني
            screenshot_path = f"screenshot_{device}.png"
            await page.screenshot(path=screenshot_path)
        
        except Exception as e:
            print(f"❌ خطأ أثناء تحميل الصفحة: {e}")
            screenshot_path = None
        
        finally:
            await browser.close()

    return screenshot_path

@ABH.on(events.NewMessage(pattern='/دز (.+)'))
async def handler(event):
    url = event.pattern_match.group(1)

    if not is_safe_url(url):
        await event.reply("🚫 هذا الموقع محظور! جرب تتواصل مع المطور @k_4x1")
        return

    devices = ['pc', 'android']
    screenshot_paths = []

    for device in devices:
        screenshot_path = await take_screenshot(url, device)
        if screenshot_path:
            screenshot_paths.append(screenshot_path)

    if screenshot_paths:
        await event.reply(f'📸 تم التقاط لقطات الشاشة للأجهزة التالية: **PC، Android**:', file=screenshot_paths)
    else:
        await event.reply("❌ هنالك خطأ أثناء التقاط لقطة الشاشة، تأكد من صحة الرابط أو جرب مجددًا.")

@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def handle_message(event):
    translator = Translator()
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text 
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None

    if not original_text:
        await event.reply("يرجى الرد على رسالة تحتوي على النص المراد ترجمته أو كتابة النص بجانب الأمر.")
        return

    try:
        detected_language = translator.detect(original_text).lang
        target_lang = "en" if detected_language == "ar" else "ar"
        translated_text = translator.translate(original_text, dest=target_lang).text

        response = (
            f"اللغة المكتشفة: {detected_language}\n"
            f"النص المترجم: `{translated_text}`"
        )
        await event.reply(response)
    except Exception as e:
        await event.reply(f"❌ حدث خطأ أثناء الترجمة: {e}")

print("✅ البوت يعمل... انتظر الأوامر!")
ABH.run_until_disconnected()
