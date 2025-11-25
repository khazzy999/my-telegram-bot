from flask import Flask
import threading
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot ishlayapti! Render server faol."

@app.route('/health')
def health():
    return "🟢 HEALTH CHECK OK"

def run_bot():
    while True:
        try:
            from bot import bot
            print("🤖 Bot ishga tushdi...")
            bot.polling(none_stop=True, interval=0, timeout=30)
        except Exception as e:
            print("❌ Bot xatosi:", e)
            time.sleep(5)  # qayta urinish
            continue

if __name__ == "__main__":
    # Bot alohida threadda ishlaydi
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()

    # Flask server ishga tushadi
    app.run(host='0.0.0.0', port=5000)