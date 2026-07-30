import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    caption = (
        f"⚡ <b>أهلاً بك يا {user_name} في بوت STAR!</b>\n\n"
        f"🛡️ <b>STAR BOT</b> هو النظام الأقوى لإدارة وحماية المجموعات.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ <b>المميزات المتاحة:</b>\n"
        f"└ 🚫 <b>حماية من السپام والروابط</b>\n"
        f"└ 🚷 <b>أوامر الحظر والكتم السريعة</b>\n"
        f"└ 💎 <b>إدارة وتثبيت الرسائل والترحيب</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 <b>قم بإضافة البوت لمجموعتك ورَفّعه مشرفاً للبدء!</b>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    
    bot_info = bot.get_me()
    add_to_group_url = f"https://t.me/{bot_info.username}?startgroup=true"

    btn_add = InlineKeyboardButton("➕ أضف البوت لمجموعتك", url=add_to_group_url)
    btn_commands = InlineKeyboardButton("📜 قائمة الأوامر", callback_data="show_commands")
    btn_developer = InlineKeyboardButton("👑 المطور", callback_data="show_dev")

    markup.add(btn_add)
    markup.add(btn_commands, btn_developer)

    bot.reply_to(message, caption, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "show_commands":
        commands_text = (
            "🛠️ <b>قائمة أوامر حماية STAR BOT:</b>\n\n"
            "• <code>/mute</code> - لكتم العضو (بالرد على رسالته)\n"
            "• <code>/ban</code> - لحظر العضو من المجموعة (بالرد على رسالته)\n"
            "• <code>/pin</code> - لتثبيت الرسالة (بالرد عليها)"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, commands_text, parse_mode="HTML")

    elif call.data == "show_dev":
        bot.answer_callback_query(call.id, text="المطور: STAR 🌟", show_alert=True)

if __name__ == '__main__':
    print("STAR BOT is running...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(3)
            
