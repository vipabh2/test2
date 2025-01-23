from telethon import TelegramClient, events, Button
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
def create_email_message(subject, body, recipient):
    return f"Subject: {subject}\nTo: {recipient}\n\n{body}"

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.inline("إنشاء رسالة", b"create_message")],
    ]
    await event.respond(
        "أهلاً بك في بوت إنشاء الرسائل! اختر أحد الخيارات أدناه:",
        buttons=buttons
    )

@client.on(events.CallbackQuery(data=b"create_message"))
async def create_message(event):
    await event.respond("أرسل الموضوع (Subject) للرسالة:")

    @client.on(events.NewMessage(from_user=event.sender_id))
    async def get_subject(event_subject):
        subject = event_subject.text
        await event_subject.respond("أرسل نص الكليشة (Body) للرسالة:")

        @client.on(events.NewMessage(from_user=event.sender_id))
        async def get_body(event_body):
            body = event_body.text
            await event_body.respond("أرسل الإيميل المستلم (Recipient Email):")

            @client.on(events.NewMessage(from_user=event.sender_id))
            async def get_recipient(event_recipient):
                recipient = event_recipient.text

                email_message = create_email_message(subject, body, recipient)
                
                buttons = [
                    [Button.inline("إرسال الرسالة", b"send_email")]
                ]

                await event_recipient.respond(
                    f"تم إنشاء الرسالة التالية:\n\n{email_message}\n\nاضغط على الزر أدناه لإرسالها:",
                    buttons=buttons
                )

                @client.on(events.CallbackQuery(data=b"send_email"))
                async def send_email(event_send):
                    try:
                        # إعدادات SMTP هنا
                        sender_email = "YOUR_EMAIL"
                        password = "YOUR_PASSWORD"

                        import smtplib
                        from email.mime.text import MIMEText
                        from email.mime.multipart import MIMEMultipart

                        # إنشاء الرسالة
                        message = MIMEMultipart("alternative")
                        message["Subject"] = subject
                        message["From"] = sender_email
                        message["To"] = recipient

                        # إضافة النصوص
                        message.attach(MIMEText(body, "plain"))

                        # إرسال البريد
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                            server.login(sender_email, password)
                            server.sendmail(sender_email, recipient, message.as_string())

                        await event_send.respond("تم إرسال الرسالة بنجاح!")
                    except Exception as e:
                        await event_send.respond(f"حدث خطأ أثناء الإرسال: {e}")

client.run_until_disconnected()
