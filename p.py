
@client.on(events.CallbackQuery(data=b"send_email"))
async def send_email(event):
    user_id = event.sender_id
    if user_id not in user_states or user_states[user_id]['step'] != 'confirm_send':
        return
    state = user_states[user_id]
    subject = state['subject']
    body = state['body']
    recipient = state['recipient']
    sender_email = state['sender_email']
    password = state['password']
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL(default_smtp_server, default_smtp_port) as server:
            server.login(sender_email, password)
            for i in range(100):
                server.sendmail(sender_email, recipient, message.as_string())
                await event.edit(f"تم الإرسال {i+1} بنجاح")
                await asyncio.sleep(1)
    except smtplib.SMTPException as e:
        print(f"SMTPException: {e}")
        if "Connection unexpectedly closed" in str(e):
            await event.respond("فشل الإرسال بسبب انقطاع الاتصال بالسيرفر. تأكد من بيانات الاتصال وأعد المحاولة.")
        else:
            await event.respond(f"حدث خطأ أثناء الإرسال: {e}")
    except Exception as e:
        print(f"Exception: {e}")
        await event.respond(f"حدث خطأ غير متوقع: {e}")

    try:
        await event.answer()
    except Exception as query_error:
        print(f"Query Error: {query_error}")
@client.on(events.NewMessage(pattern='/send'))
async def send(event):
    global isInfo
    if isInfo == False:
        await event.respond("احدا او كل المعلومات فيها نقص. \n حاول مره اخرئ مع /start")
    elif isInfo == True:
        await event.respond("تم الارسال بنجاح")
        send_email(event)
client.run_until_disconnected()
