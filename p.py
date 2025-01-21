from telethon import TelegramClient, events
import os
import sqlite3

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)
# @ABH.on(events.MessageEdited)
# async def echo(event):
#     if event.message == media:
#         await event.reply("ها ههههه سالمين")
#     else:
#         return    
# Create a database connection and a table to store user approvals
conn = sqlite3.connect('approvals.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS approvals (
    user_id INTEGER PRIMARY KEY,
    approved BOOLEAN NOT NULL
)
''')
conn.commit()

@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    user_id = event.sender_id
    cursor.execute('INSERT OR REPLACE INTO approvals (user_id, approved) VALUES (?, ?)', (user_id, True))
    conn.commit()
    await event.reply("تم السماح بالتعديلات")

@ABH.on(events.MessageEdited)
async def echo(event):
    user_id = event.sender_id
    cursor.execute('SELECT approved FROM approvals WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result and result[0]:
        if event.message.media:  
            await event.reply("ها ههههه سالمين")
        else:
            return
ABH.run_until_disconnected()
