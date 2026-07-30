import telebot
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ STAR BOT يعمل بنجاح وبأعلى استقرار!")

if __name__ == '__main__':
    print("STAR BOT is starting...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(3)
    
