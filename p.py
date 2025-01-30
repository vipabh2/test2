@ABH.on(events.InlineQuery)
async def inline_query_handler(event):
    ifid = await event.get_reply_message()
    to_id = None

    if ifid:
        # استخراج معرف المستلم الحقيقي من الرسالة المردود عليها
        if ifid.forward and ifid.forward.from_id:
            to_id = ifid.forward.from_id  # إذا كانت الرسالة محولة
        elif hasattr(ifid.to_id, 'user_id'):
            to_id = ifid.to_id.user_id  # إذا كانت رسالة خاصة
        else:
            to_id = ifid.chat_id  # إذا كانت في مجموعة

    builder = event.builder
    query = event.text.strip()
    sender = event.sender_id

    if not query:
        return

    parts = query.split(' ')
    
    # استخراج الرسالة واسم المستلم (اسم مستخدم أو ID أو الرد على شخص)
    message = ' '.join(parts[:-1]) if len(parts) >= 2 else query
    recipient = parts[-1] if len(parts) >= 2 else None

    # التحقق مما إذا كان الإدخال معرفًا رقميًا
    is_numeric_id = recipient and recipient.isdigit()

    if recipient:
        if recipient.startswith('@'):
            username = recipient
            reciver = await ABH.get_entity(username)  # جلب الكيان باستخدام اسم المستخدم
            reciver_id = reciver.id
        elif is_numeric_id:
            reciver_id = int(recipient)  # تحويل المعرف النصي إلى عدد صحيح
            username = f'User({reciver_id})'
        else:
            return  # تجاهل الإدخالات غير الصحيحة
    elif to_id:  # إذا لم يتم إدخال اسم مستخدم أو ID، استخدم المستلم من الرسالة المردود عليها
        reciver_id = to_id
        username = f'User({to_id})'
    else:
        return  # لا يوجد مستلم، تجاهل الطلب

    try:
        whisper_id = str(uuid.uuid4())
        store_whisper(whisper_id, sender, reciver_id, username, message)

        result = builder.article(
            title='اضغط لإرسال الهمسة',
            description=f'إرسال الرسالة إلى {username}',
            text=f"همسة سرية إلى \n ({username})",
            buttons=[Button.inline(text='🫵🏾 اضغط لعرض الهمسة', data=f'send:{whisper_id}')],
            thumb_url="https://example.com/whisper.png"  # ضع رابط الصورة هنا
        )

    except Exception as e:
        print(f"خطأ أثناء معالجة الطلب: {e}")
        result = builder.article(
            title='خطأ في الإرسال',
            description=f"حدث خطأ أثناء معالجة طلبك: {str(e)}",
            thumb_url="https://example.com/error.png"
        )

    await event.answer([result])
