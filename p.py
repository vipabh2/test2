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
    if event.is_group and event.message.media:
        buttons = [
            [Button.inline("حظر ومسح", b"ban_and_delete"), Button.inline("مسح", b"delete_only")]
        ]
        await event.reply("تم تعديل هذه الرسالة", buttons=buttons)

@ABH.on(events.CallbackQuery)
async def callback_handler(event):
    if event.data == b"ban_and_delete":
        await event.delete()  # Delete the message
        # Ban the user (this is just an example, you need to implement the actual banning logic)
        await event.client.edit_permissions(event.chat_id, event.sender_id, view_messages=False)
    elif event.data == b"delete_only":
        await event.delete()  # Delete the message

ABH.run_until_disconnected()
