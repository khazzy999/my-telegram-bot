from flask import Flask
import threading
import time
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Server ishlayapti! " + str(time.time())

@app.route('/health')
def health():
    return "🟢 OK"

# Botni alohida process da ishga tushirish
def run_bot():
    while True:
        try:
            print("🚀 Bot ishga tushirilmoqda...")
            # Botni alohida process da ishga tushirish
            process = subprocess.Popen([sys.executable, "bot.py"], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            
            stdout, stderr = process.communicate()
            
            if stdout:
                print(f"Bot stdout: {stdout.decode()}")
            if stderr:
                print(f"Bot stderr: {stderr.decode()}")
                
            print("❌ Bot to'xtadi. 10 soniyadan keyin qayta ishga tushadi...")
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Bot process xatosi: {e}")
            time.sleep(10)

if __name__ == "__main__":
    print("🌐 Flask server ishga tushdi")
    # Botni background da ishga tushirish
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask server
    app.run(host='0.0.0.0', port=5000)
