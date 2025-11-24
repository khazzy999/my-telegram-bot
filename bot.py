from telebot import types
import telebot
import time

print("🤖 Bot kod yuklanmoqda...")
BOT_TOKEN = "8446328283:AAFSjSxDahTorCP8uc2xcjdPBGZzrLGZgj8"
print(f"✅ Token: {BOT_TOKEN[:10]}...")

bot = telebot.TeleBot(BOT_TOKEN)
print("✅ Bot obyekt yaratildi")

@bot.message_handler(commands=['start'])
def start(message):
    print(f"📩 /start command: {message.from_user.id}")
    bot.reply_to(message, "🎉 Bot ishlayapti! Test muvaffaqiyatli!")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Server ishlayapti")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"Siz: {message.text}")

print("🔄 Bot polling boshlanmoqda...")
try:
    bot.infinity_polling()
except Exception as e:
    print(f"❌ Bot xatosi: {e}")
    time.sleep(5)