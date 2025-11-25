import os
from dotenv import load_dotenv
import telebot
from telebot import types
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ==== SAFE ADMIN IDS LOADER ====
admin_raw = os.getenv("ADMIN_IDS", "")
if admin_raw.strip() == "":
    ADMIN_IDS = []
else:
    ADMIN_IDS = [int(x) for x in admin_raw.split(",") if x.isdigit()]

bot = telebot.TeleBot(BOT_TOKEN)


# ===== GEMINI =====
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    r = requests.post(url, json=data)
    try:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ Gemini javob bera olmadi."


# ===== DEEPSEEK =====
def ask_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(url, headers=headers, json=payload)
    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "❌ DeepSeek javob bera olmadi."


USER_MODE = {}

MODES = {
    "gemini": "Gemini AI",
    "deepseek": "DeepSeek AI",
    "normal": "Oddiy Chat"
}


# ===== /admin =====
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        return bot.reply_to(message, "❌ Siz admin emassiz.")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📊 Statistika", callback_data="stats"))
    markup.add(types.InlineKeyboardButton("📩 Reklama yuborish", callback_data="broadcast"))

    bot.send_message(message.chat.id, "🔥 Admin panel", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "stats")
def stats(call):
    bot.send_message(
        call.message.chat.id,
        "📊 Statistika:\n- Jami foydalanuvchilar: 0\n- Bugungi aktiv: 0\n- Premium: 0"
    )


@bot.callback_query_handler(func=lambda call: call.data == "broadcast")
def broadcast(call):
    msg = bot.send_message(call.message.chat.id, "✍️ Reklama matnini yuboring:")
    bot.register_next_step_handler(msg, send_broadcast)


def send_broadcast(message):
    bot.reply_to(message, "✅ Reklama yuborildi. (Demo)")


# ===== /mode =====
@bot.message_handler(commands=['mode'])
def change_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key, val in MODES.items():
        markup.add(val)
    msg = bot.send_message(message.chat.id, "Rejimni tanlang:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_mode)


def save_mode(message):
    for key, val in MODES.items():
        if message.text == val:
            USER_MODE[message.from_user.id] = key
            return bot.send_message(message.chat.id, f"✅ Rejim: {val}")

    bot.send_message(message.chat.id, "❌ Bunday rejim yo‘q.")


# ===== MAIN CHAT =====
@bot.message_handler(func=lambda m: True)
def main_chat(message):
    mode = USER_MODE.get(message.from_user.id, "gemini")
    text = message.text

    bot.send_chat_action(message.chat.id, "typing")

    if mode == "gemini":
        answer = ask_gemini(text)
    elif mode == "deepseek":
        answer = ask_deepseek(text)
    else:
        answer = "👋 Oddiy chat rejimi."

    bot.send_message(message.chat.id, answer)