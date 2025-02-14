import os
import re
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserNotParticipantError, ParticipantIdInvalidError

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

banned_words = [
    "افتحج", "افتحك", "انيچة", "nude", "porn", "سكس", "لوطي", "كس", "طيز", "بورن",
    # Add other banned words...
]

def normalize_text(text):
    # Normalizing text by removing unwanted characters
    text = re.sub(r'[^أ-يa-zA-Z\s]', '', text)
    return text

def clean_message(message):
    # Clean the message by replacing banned words with "****"
    words = message.split()
    cleaned_words = [word if word not in banned_words else "****" for word in words]
    return " ".join(cleaned_words)

@ABH.on(events.NewMessage)
async def handler(event):
    if event.is_group and event.sender_id == 1910015590:
        if event.raw_text.startswith('#'):
            new_word = event.raw_text[1:].strip()
            if new_word not in banned_words:
                banned_words.append(new_word)
                await event.reply(f"✅ تم إضافة الكلمة '{new_word}' إلى قائمة الكلمات المحظورة!")
            else:
                await event.reply(f"⚠️ الكلمة '{new_word}' موجودة بالفعل في القائمة.")
        else:
            cleaned_text = clean_message(event.raw_text)
            if cleaned_text != event.raw_text:
                user_id = event.sender_id
                chat = await event.get_chat()
                try:
                    participant = await ABH(GetParticipantRequest(chat.id, user_id))
                    if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                        return
                except (UserAdminInvalidError, UserNotParticipantError, ParticipantIdInvalidError):
                    pass

                restrict_rights = ChatBannedRights(
                    until_date=None,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    embed_links=True
                )
                await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
                await event.delete()
                await event.reply(f"⤶ المستخدم [{event.sender.first_name}](tg://user?id={event.sender_id}) تم تقييده لاستخدامه كلمة محظورة ☠")

print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
