import telebot
from telebot import types
import google.generativeai as genai

# توكن البوت
TOKEN = '8990642288:AAG6FMlXughz6XfHpaI2wsxYjYfj2G9_6Vk'
bot = telebot.TeleBot(TOKEN)

# مفتاح جيميناي
GEMINI_API_KEY = 'AQ.Ab8RN6JioVPrIivIGHpukYIN-QS6J69KEt3wDASAa5oZsu5r2w'
genai.configure(api_key=GEMINI_API_KEY)

ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "أنت مهندس صيانة ومخططات سوفت وير محترف في بوت الـمُفَكِّر.\n"
        "إجاباتك بالعامية المصرية للمحلات.\n"
        "1. في التوافقات: وضح توافق الشاشات والبطاريات.\n"
        "2. في الإصلاح: اشرح خطوات فحص البوردة والمسارات.\n"
        "3. في السوفت وير: اشرح خطوات التفليش وأزرار البوت."
    )
)

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_compat = types.InlineKeyboardButton("🔄 1. قسم التوافقات", callback_data="main_compatibility")
    btn_repair = types.InlineKeyboardButton("🛠️ 2. قسم الإصلاح", callback_data="main_repair")
    btn_soft = types.InlineKeyboardButton("💻 3. قسم السوفت وير", callback_data="main_software")
    markup.add(btn_compat, btn_repair, btn_soft)
    bot.send_message(message.chat.id, "👑 مرحباً بك في بوت الـمُفَكِّر 👑", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    if call.data == "main_compatibility":
        bot.edit_message_text("🔄 قسم التوافقات - اختر النوع:", chat_id, call.message.message_id)
    elif call.data == "main_repair":
        bot.edit_message_text("🛠️ قسم الإصلاح - اختر البراند:", chat_id, call.message.message_id)
    elif call.data == "main_software":
        bot.edit_message_text("💻 قسم السوفت وير - اختر البراند:", chat_id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def handle_text_inputs(message):
    bot.reply_to(message, "أنا جاهز، اكتبلي اللي محتاجه عشان أساعدك في الصيانة.")

print("بوت الـمُفَكِّر شغال...")
bot.infinity_polling()
