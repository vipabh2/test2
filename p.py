import requests, os, operator, asyncio, random, uuid, datetime 
from telethon import TelegramClient, events, Button
from telethon.errors import BadRequestError
from telethon.tl.functions.users import GetFullUserRequest


api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  

# إنشاء الجلسة
ABH = TelegramClient("ubot", api_id, api_hash)
@ABH.on(pattern="قنواتي$")
async def _(event):
    "To list all public channels and groups."
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "᯽︙ جميع القنوات والمجموعات التي قمت بأنشائها :\n"
    output_str += "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await event.reply(output_str)
ABH.connect()
ABH.run_until_disconnected()
