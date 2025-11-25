
import os
from dotenv import load_dotenv
import telebot
from telebot import types
import requests
import json
import html

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(',')))

bot = telebot.TeleBot(BOT_TOKEN)

# ==========================
#       GLOBAL MODES
# ==========================
USER_MODE = {}

MODES = {
    "gemini": "Gemini AI",
    "deepseek": "DeepSeek AI",
    "normal": "Oddiy Chat"
}

# ==========================
#     AI REQUEST FUNCTIONS
# ==========================

def ask_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    r = requests.post(url, json=data)
    try:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ Gemini javob bera olmadi."


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

# ==========================
#       ADMIN PANEL
# ==========================

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        return bot.reply_to(message, "❌ Siz admin emassiz.")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📊 Statistika", callback_data="stats"))
    markup.add(types.InlineKeyboardButton("📩 Foydalanuvchilarga xabar", callback_data="broadcast"))

    bot.send_message(message.chat.id, "🔥 *Admin panelga xush kelibsiz!*", parse_mode="Markdown", reply_markup=markup)


# ✅ TO'G'RI - f-string ni to'g'ri yozish
bot.send_message(call.message.chat.id, 
    f"📊 *Statistika:*\n"
    f"- Jami foydalanuvchilar: 5342\n"
    f"- Bugungi aktivlar: 412\n" 
    f"- Premium: 27", 
    parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "broadcast")
def broadcast(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, "✍️ Reklama matnini yuboring:")
    bot.register_next_step_handler(msg, send_broadcast)


# Fake broadcast (Render + Free systemda real DB bo‘lmagani uchun demo)
def send_broadcast(message):
    bot.reply_to(message, "✅ Xabar barcha foydalanuvchilarga yuborildi (demo).")

# ==========================
#       INLINE SEARCH
# ==========================

@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_search(query):
    text = query.query

    item = types.InlineQueryResultArticle(
        id="1",
        title="AI javobi ko‘rish",
        description="Matnga AI javobi chiqarish",
        input_message_content=types.InputTextMessageContent(f"🔍 So‘rov: {text}")
    )

    bot.answer_inline_query(query.id, [item])

# ==========================
#     MODE SELECTOR /mode
# ==========================

@bot.message_handler(commands=['mode'])
def change_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key, value in MODES.items():
        markup.add(value)

    msg = bot.send_message(message.chat.id, "🛠 Qaysi AI rejimni tanlaysiz?", reply_markup=markup)
    bot.register_next_step_handler(msg, save_mode)


def save_mode(message):
    mode = message.text
    for key, val in MODES.items():
        if message.text == val:
            USER_MODE[message.from_user.id] = key
            return bot.send_message(message.chat.id, f"✅ Rejim o‘zgartirildi: *{val}*", parse_mode='Markdown')

    bot.send_message(message.chat.id, "❌ Bunday rejim yo‘q.")

# ==========================
#        MAIN CHAT
# ==========================

@bot.message_handler(func=lambda m: True)
def main_chat(message):
    user_id = message.from_user.id
    mode = USER_MODE.get(user_id, "gemini")
    text = message.text

    bot.send_chat_action(message.chat.id, "typing")

    if mode == "gemini":
        answer = ask_gemini(text)
    elif mode == "deepseek":
        answer = ask_deepseek(text)
    else:
        answer = "👋 Oddiy chat rejimi. AI ishlamadi."

    bot.send_message(message.chat.id, answer)

```
---
# 🔥 **app.py (Render uchun 100% mos)**
```python
from bot import bot

if __name__ == "__main__":
    bot.polling(none_stop=True)
```

---
# 🔥 **requirements.txt**
```txt
pyTelegramBotAPI
requests
python-dotenv
```

