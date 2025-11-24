from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot ishlayapti! Server faol."

@app.route('/health')
def health():
    return "🟢 OK"

# Botni alohida threadda ishga tushirish
def run_bot():
    try:
        from bot import run_bot
        run_bot()
    except Exception as e:
        print(f"Bot xatosi: {e}")

if __name__ == "__main__":
    # Botni background da ishga tushirish
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask serverni ishga tushirish
    app.run(host='0.0.0.0', port=5000)
