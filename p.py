from telethon import TelegramClient, events, Button
import requests, os, operator, asyncio, random
from googletrans import Translator
from bs4 import BeautifulSoup
import time

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.MessageEdited)
async def handle_edited_message(event):
    if event.message.media:  # Check if the message has media (files, photos, videos)
        await event.reply("تم تعديل هذه الرسالة التي تحتوي على ملفات أو صور أو فيديوهات")
    pass

ABH.run_until_disconnected()
