import os
from flask import Flask, request
from bot import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'OK'

if __name__ == "__main__":
    if os.environ.get('RENDER'):  # Render productionda
        bot.remove_webhook()
        bot.set_webhook(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook")
    else:  # Localda
        bot.polling(none_stop=True)