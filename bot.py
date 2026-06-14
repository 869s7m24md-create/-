import telebot
import os
import google.generativeai as genai

# جلب المتغيرات من Railway
TOKEN = os.environ.get("TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "أنت مساعد محترف في بوت المُفَكِّر الخاص بصيانة المحمول. "
        "إجاباتك بالعامية المصرية للمحلات. "
        "1. وضح توافق الشاشات والبطاريات. "
        "2. اشرح خطوات فحص البوردة والمسارات. "
        "3. اشرح خطوات التفليش وأزرار البوت."
    )
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👑 أهلاً بك في بوت المُفَكِّر، أنا جاهز لمساعدتك في الصيانة!")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        response = ai_model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "معلش، حصلت مشكلة، جرب تاني.")

bot.infinity_polling()
