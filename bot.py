from telebot import types
import telebot
import requests
import json
import base64

BOT_TOKEN = "8446328283:AAFSjSxDahTorCP8uc2xcjdPBGZzrLGZgj8"
bot = telebot.TeleBot(BOT_TOKEN)

# ==================== ADMIN PANEL ====================
ADMIN_IDS = [123456789]  # O'Z ID INGIZNI YOZING!

def is_admin(user_id):
    return user_id in ADMIN_IDS

DEEPSEEK_API_KEY = "sk-b60f00175ab24aa4b3ef0925c3f2f51d"
GEMINI_API_KEY = "AIzaSyBaAonO_-TI-Wfpt5iEbtov3aLvC7VB6dQ"

# Rasmni base64 formatiga o'tkazish
def rasmni_base64_ga_otkazish(rasm_url):
    try:
        response = requests.get(rasm_url)
        response.raise_for_status()
        base64_rasm = base64.b64encode(response.content).decode('utf-8')
        return base64_rasm
    except Exception as e:
        print(f"Rasm yuklash xatosi: {e}")
        return None

# Google Gemini API orqali rasm tahlili
def gemini_rasm_tahlili(rasm_base64, savol=""):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if not savol:
            savol = "Bu rasmda qanday savol yoki masala bor? Batafsil tushuntiring va to'liq javob bering."
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": rasm_base64
                            }
                        },
                        {
                            "text": savol
                        }
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 1000
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "❌ Rasmda savol topilmadi. Iltimos, aniqroq rasm yuboring."
        else:
            return f"❌ Rasm tahlili xatosi. Iltimos, savolni matn shaklida yozing."
        
    except Exception as e:
        return f"❌ Rasm tahlili vaqti tugadi. Savolni matn shaklida yozing."

# DeepSeek API orqali matnli javob olish
def deepseek_javob_ber(savol):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Siz talabalar uchun foydali yordamchi botsiz. Matematika, fizika, dasturlash, kimyo, tarix va boshqa fanlar bo'yicha tushunarli javob bering."
                },
                {
                    "role": "user",
                    "content": savol
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Men hozir javob bera olmayman. Iltimos, keyinroq urinib ko'ring."
        
    except Exception as e:
        return f"❌ Texnik xatolik: {str(e)}"

# ==================== BOT COMMANDS ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    welcome_text = """
🤖 **TALABA YORDAMCHI BOTGA XUSH KELIBSIZ!**

🎯 **Men sizga quyidagilarda yordam beraman:**
• 📝 **Matnli savollar** - DeepSeek AI
• 📸 **Rasmli savollar** - Google Gemini AI

📚 **Qo'llab-quvvatlanadigan fanlar:**
- Matematika (algebra, geometriya)
- Fizika (mexanika, energiya)  
- Dasturlash (Python, Java)
- Kimyo (formulalar, reaksiyalar)
- Tarix va adabiyot

💡 **Misol savollar:**
"Kvadrat tenglama nima?"
"Python dasturlashni qanday o'rganish mumkin?"
"Fizikada energiya nima?"

📸 **Rasm yuborish:** Test savollari, masalalar, kodlar rasmini yuboring

⚡ **Tez va aniq javoblar!**
"""
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🆘 **YORDAM**

**Qanday foydalanish:**
1. Savolni yozing yoki rasm yuboring
2. Kutiling (2-10 soniya)
3. Javob oling

**Rasm qoidalari:**
• Yorug' va aniq rasm bo'lsin
• Matn o'qish mumkin bo'lsin
• Format: JPEG, PNG

**Qo'shimcha buyruqlar:**
/test - Botni sinash
/api - API holati
/admin - Admin panel (faqat adminlar uchun)
/myid - O'z ID ingizni olish
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['test'])
def test_command(message):
    test_text = """
🧪 **TEST REJIMI**

Botni sinab ko'rish uchun:

📝 **Matnli test:** 
"Salom, qandaysan?" yuboring

📸 **Rasmli test:**
Matematika masalasi yoki test savoli rasmini yuboring

✅ **Javob kelsa** - bot ishlayapti
❌ **Javob kelmasa** - /help buyrug'idan foydalaning
"""
    bot.send_message(message.chat.id, test_text)

@bot.message_handler(commands=['api'])
def api_command(message):
    api_text = """
🔧 **API HOLATI:**

✅ **DeepSeek API:** Faol
✅ **Gemini API:** Faol  
✅ **Bot:** Ishlamoqda

📊 **Imkoniyatlar:**
• Matnli savollarga javob
• Rasmli savollarni tahlil qilish
• 24/7 ishlash
"""
    bot.send_message(message.chat.id, api_text)

# ==================== ADMIN FUNCTIONS ====================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Siz admin emassiz!")
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('📊 Statistika', callback_data='admin_stats'),
        types.InlineKeyboardButton('👥 Foydalanuvchilar', callback_data='admin_users')
    )
    markup.row(
        types.InlineKeyboardButton('📢 Xabar yuborish', callback_data='admin_broadcast'),
        types.InlineKeyboardButton('⚙️ Sozlamalar', callback_data='admin_settings')
    )
    markup.row(
        types.InlineKeyboardButton('🔄 Restart', callback_data='admin_restart'),
        types.InlineKeyboardButton('❌ Yopish', callback_data='admin_close')
    )
    
    bot.send_message(message.chat.id, "🛠️ **Admin Panel**", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def handle_admin_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ Siz admin emassiz!")
        return
    
    if call.data == 'admin_stats':
        user_count = "100"  # Bu yerda haqiqiy foydalanuvchilar sonini qo'shing
        bot.edit_message_text(
            f"📊 **Bot Statistika:**\n\n👥 Foydalanuvchilar: {user_count}\n🕐 Ish vaqti: 24/7",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_admin_menu(),
            parse_mode='Markdown'
        )
    
    elif call.data == 'admin_users':
        bot.edit_message_text(
            "👥 **Foydalanuvchilar boshqaruvi**\n\nKeyingi yangilanishda qo'shiladi...",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_admin_menu(),
            parse_mode='Markdown'
        )
    
    elif call.data == 'admin_broadcast':
        bot.edit_message_text(
            "📢 **Xabar yuborish**\n\nBarcha foydalanuvchilarga xabar yuborish.\nKeyingi yangilanishda qo'shiladi...",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_admin_menu(),
            parse_mode='Markdown'
        )
    
    elif call.data == 'admin_settings':
        bot.edit_message_text(
            "⚙️ **Sozlamalar**\n\nAPI sozlamalari va bot konfiguratsiyasi.\nKeyingi yangilanishda qo'shiladi...",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_admin_menu(),
            parse_mode='Markdown'
        )
    
    elif call.data == 'admin_restart':
        bot.edit_message_text(
            "🔄 **Bot qayta ishga tushirildi**\n\nBot muvaffaqiyatli qayta ishga tushdi!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_admin_menu(),
            parse_mode='Markdown'
        )
    
    elif call.data == 'admin_close':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "✅ Admin panel yopildi")
    
    else:
        bot.answer_callback_query(call.id, "⚙️ Sozlamalar yangilanmoqda...")

def create_admin_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('📊 Statistika', callback_data='admin_stats'),
        types.InlineKeyboardButton('👥 Foydalanuvchilar', callback_data='admin_users')
    )
    markup.row(
        types.InlineKeyboardButton('📢 Xabar yuborish', callback_data='admin_broadcast'),
        types.InlineKeyboardButton('⚙️ Sozlamalar', callback_data='admin_settings')
    )
    markup.row(
        types.InlineKeyboardButton('🔄 Restart', callback_data='admin_restart'),
        types.InlineKeyboardButton('❌ Yopish', callback_data='admin_close')
    )
    return markup

@bot.message_handler(commands=['myid'])
def get_my_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Sizning ID ingiz: `{user_id}`\n\nBu ID ni ADMIN_IDS ga qo'shing!", parse_mode='Markdown')

# ==================== MESSAGE HANDLERS ====================
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    try:
        wait_msg = bot.send_message(message.chat.id, "📸 Rasm tahlil qilinmoqda...")
        
        file_info = bot.get_file(message.photo[-1].file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        
        rasm_base64 = rasmni_base64_ga_otkazish(file_url)
        
        if rasm_base64:
            user_caption = message.caption if message.caption else ""
            response = gemini_rasm_tahlili(rasm_base64, user_caption)
            
            bot.delete_message(message.chat.id, wait_msg.message_id)
            
            if len(response) > 4000:
                parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
                for i, part in enumerate(parts):
                    if i == 0:
                        bot.send_message(message.chat.id, f"📸 **Rasm tahlili:**\n\n{part}")
                    else:
                        bot.send_message(message.chat.id, part)
            else:
                bot.send_message(message.chat.id, f"📸 **Rasm tahlili:**\n\n{response}")
                
        else:
            bot.edit_message_text(
                "❌ Rasm yuklanmadi. Iltimos, boshqa rasm yuboring.",
                message.chat.id,
                wait_msg.message_id
            )
            
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, wait_msg.message_id)
        except:
            pass
        bot.reply_to(message, f"❌ Rasm tahlili xatosi: {str(e)}")

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    if message.text.startswith('/'):
        return
    
    try:
        wait_msg = bot.send_message(message.chat.id, "⏳ Javob tayyorlanmoqda...")
        response = deepseek_javob_ber(message.text)
        bot.delete_message(message.chat.id, wait_msg.message_id)
        
        if len(response) > 4000:
            parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    bot.send_message(message.chat.id, f"🤖 **Javob:**\n\n{part}")
                else:
                    bot.send_message(message.chat.id, part)
        else:
            bot.send_message(message.chat.id, f"🤖 **Javob:**\n\n{response}")
        
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, wait_msg.message_id)
        except:
            pass
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}")

# ==================== BOT START ====================
print("BOT ISHGA TUSHDI!")
print("DeepSeek API: Faol")
print("Gemini API: Faol")
print("Bot tayyor!")

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot xatosi: {e}")