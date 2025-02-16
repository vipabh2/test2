from telethon import TelegramClient, events, Button
import os, asyncio, smtplib, random

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

questions_and_answers = [
    {"question": "متى أقيمت أول بطولة لكأس العالم لكرة القدم؟", "answer": ["1930"]},
    {"question": "كم مرة فاز المنتخب السعودي بكأس آسيا لكرة القدم؟", "answer": ["3 مرات"]},
    {"question": "أين أقيمت بطولة كأس العالم لكرة القدم عام 2002؟", "answer": ["كوريا الجنوبية واليابان", 'كوريا الجنوبية و اليابان']},
    {"question": "ما هو النادي الأكثر تحقيقًا للبطولات في العالم؟", "answer": ["ريال مدريد"]},
    {"question": "المنتخب الاكثر فوز ب كأس العالم؟", "answer": ["البرازيل"]},
    {"question": "من هو النادي الأكثر مشاركة في الدوري الأوروبي؟", "answer": ["ريال مدريد"]},
    {"question": "من هو اللاعب المعروف بأنه الهداف الأول في دوري أبطال أوروبا؟", "answer": ["كريستيانو رونالدو", 'رونالدو', "كرستيانو"]},
    {"question": "فريق كرة القدم يتكون من كم لاعب؟", "answer": ["11 لاعب"]},
    {"question": "من اللاعب الحاصل على جائزة الكرة الذهبية في عام 2015م؟", "answer": ["كريستيانو رونالدو", 'رونالدو', "كرستيانو"]},
    {"question": "متى سجل دييجو مارادونا هدفه الشهير باليد في كأس العالم؟", "answer": ["1986"]},
    {"question": "ما هي الدولة التي ظهرت فيها كرة القدم لأول مرة؟", "answer": ["إنجلترا"]},
    {"question": "ما هو تاريخ أول كأس عالم ومتى أقيم لأول مرة؟", "answer": ["1930"]},
    {"question": "في أي دولة أقيم كأس العالم الأول؟", "answer": ["الاورغواي"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في تاريخ كأس العالم؟", "answer": ["كلوزه"]},
    {"question": "ما هي الدولة التي فازت بأكبر عدد من بطولات كأس العالم؟", "answer": ["البرازيل"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في كأس العالم 2018؟", "answer": ["مودريتش"]},
    {"question": "ما هو النادي الذي حقق دوري أبطال أوروبا ثلاث مرات متتالية في الفترة الحديثة؟", "answer": ["ريال مدريد"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الظاهرة'؟", "answer": ["رونالدو"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'الشياطين الحمر'؟", "answer": ["مانشستر يونايتد"]},
    {"question": "من هو اللاعب الذي سجل أسرع هدف في تاريخ كأس العالم؟", "answer": ["هاكان"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الإنجليزي الممتاز؟", "answer": ["مانشستر يونايتد"]},
    {"question": "من هو اللاعب الذي يُلقب بـ'البرغوث'؟", "answer": ["ليونيل ميسي", 'ميسي', "مسي"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 2010؟", "answer": ["افريقيا"]},
    {"question": "من هو المدرب الذي قاد منتخب ألمانيا للفوز بكأس العالم 2014؟", "answer": ["لوف"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'البلوز'؟", "answer": ["تشيلسي"]},
    {"question": "من هو اللاعب الذي حصل على جائزة الحذاء الذهبي في كأس العالم 2014؟", "answer": ["رودريغيز"]},
    {"question": "ما هو أكبر ملعب لكرة القدم في العالم من حيث السعة؟", "answer": ["ملعب رونغرادو"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الماجيك'؟", "answer": ["رونالدينيو"]},
    {"question": "ما هي الدولة التي فازت بأول بطولة لكأس العالم؟", "answer": ["الاورغواي"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في موسم واحد بالدوري الإنجليزي الممتاز؟", "answer": ["محمد صلاح"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'العجوز'؟", "answer": ["يوفنتوس"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في أوروبا لعام 2020؟", "answer": ["روبرت ليفاندوفسكي", 'ليفاندوفسكي']},
    {"question": "ما هي الدولة التي استضافت كأس العالم 1998؟", "answer": ["فرنسا"]},
    {"question": "من هو اللاعب الذي يُلقب بـ'الفتى الذهبي'؟", "answer": ["دييغو مارادونا"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الإسباني؟", "answer": ["ريال مدريد"]},
    {"question": "ما هي الدولة التي فازت ببطولة كأس الأمم الأوروبية 2016؟", "answer": ["البرتغال"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الملك' في كرة القدم؟", "answer": ["بيليه"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'الريدز'؟", "answer": ["ليفربول"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في أفريقيا لعام 2019؟", "answer": ["ساديو ماني"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 2006؟", "answer": ["ألمانيا"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الفرنسي؟", "answer": ["سانت إتيان"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في تاريخ الدوري الألماني؟", "answer": ["غيرد مولر"]},
    {"question": "ما هي الدولة التي فازت ببطولة كوبا أمريكا 2019؟", "answer": ["البرازيل"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'المايسترو'؟", "answer": ["أندريا بيرلو"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'النسور'؟", "answer": ["لاتسيو"]},
]
user_states = {}
@ABH.on(events.NewMessage(pattern='رياضة|/sport'))
async def start(event):
    user_id = event.sender_id
    question = random.choice(questions_and_answers)
    user_states[user_id] = {
        "question": question,
        "waiting_for_answer": True 
    }
    await event.reply(f"{question['question']}")
@ABH.on(events.NewMessage)
async def check_answer(event):
    user_id = event.sender_id
    user_message = event.text.strip().lower()
    if user_id in user_states and user_states[user_id].get("waiting_for_answer"):
        current_question = user_states[user_id].get("question", {})
        correct_answer = current_question.get('answer', '')
        if isinstance(correct_answer, str):
            correct_answer = correct_answer.lower()
        else:
            correct_answer = str(correct_answer)

        if user_message == correct_answer:
            await event.reply("اجابة صحيحة احسنت.")
            del user_states[user_id]
        else:
          return          
ABH.run_until_disconnected()
