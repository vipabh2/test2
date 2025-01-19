from telethon import TelegramClient, events, Button
from telethon.tl.types import ChannelParticipantsAdmins
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
            [Button.inline("إبلاغ المشرفين", b"notify_admins"), Button.inline("مسح", b"delete_only")]
        ]
        await event.reply("تم تعديل هذه الرسالة", buttons=buttons)

@ABH.on(events.CallbackQuery)
async def callback_handler(event):
    if event.data == b"notify_admins":
        await notify_admins(event)
    elif event.data == b"delete_only":
        me = await event.client.get_me()
        participant = await event.client.get_permissions(event.chat_id, me)
        if participant.is_admin:
            original_message = await event.get_reply_message()
            await original_message.delete()  # Delete the original edited message
            await event.reply("تم مسح الرسالة.")
        else:
            await event.reply("لا يمكنك مسح هذه الرسالة، فقط المشرفين يمكنهم ذلك.")

async def notify_admins(event):
    admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    for admin in admins:
        await event.client.send_message(admin.id, f"تم تعديل رسالة في المجموعة {event.chat.title}.")
    await event.reply("تم إبلاغ المشرفين.")

ABH.run_until_disconnected()
