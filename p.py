from telethon import TelegramClient, events
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/react'))
async def handler(event):
    # إضافة رد فعل (emoji) إلى الرسالة
    await event.message.react('😎')

    # الرد على المستخدم
    await event.reply("تم إضافة رد فعل 😎!")

client.run_until_disconnected()
