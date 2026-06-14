import telebot
import os
import google.generativeai as genai

# جلب المفاتيح من متغيرات النظام في Railway
TOKEN = os.environ.get("TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# إعداد البوت وموديل جيمناي
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "أنت مساعد محترف في بوت المُفَكِّر الخاص بصيانة المحمول."
        "إجاباتك يجب أن تكون بالعامية المصرية للمحلات."
        "1. وضح توافق الشاشات والبطاريات."
        "2. اشرح خطوات فحص البوردة والمسارات."
        "3. اشرح خطوات التفليش وأزرار البوت."
    )
)

# أمر البدء
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("التوافق", callback_data="main_compatibility")
    btn2 = telebot.types.InlineKeyboardButton("الفحص", callback_data="main_repair")
    btn3 = telebot.types.InlineKeyboardButton("السوفت", callback_data="main_software")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "👑 أهلاً بك في بوت المُفَكِّر، كيف أساعدك اليوم؟", reply_markup=markup)

# الرد على أي رسالة نصية باستخدام جيمناي
@bot.message_handler(func=lambda message: True)
def handle_text_inputs(message):
    try:
        response = ai_model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "معلش، حصلت مشكلة وأنا بكلم جيمناي، جرب تاني!")
        print(f"Error: {e}")

print("...البوت جاهز ومستني أوامرك!")
bot.infinity_polling()
