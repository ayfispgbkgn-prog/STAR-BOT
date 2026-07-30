import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# دالة التأكد من المشرفين
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception:
        return False

# ----------------- الواجهة الاحترافية عند إرسال /start -----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    # نص الواجهة الترحيبية التنسيقي
    caption = (
        f"⚡ **أهلاً بك يا {user_name} في بوت STAR!**\n\n"
        f"🛡️ **STAR BOT** هو النظام الأقوى والأحدث لإدارة وحماية المجموعات التفاعلية.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ **المميزات المتاحة:**\n"
        f"└ 🚫 **حماية من السپام والروابط**\n"
        f"└ 🚷 **أوامر الحظر والكتم السريعة**\n"
        f"└ 💎 **إدارة وتثبيت الرسائل والترحيب**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 **قم بإضافة البوت لمجموعتك ورَفّعه مشرفاً للبدء!**"
    )

    # إنشاء الأزرار الشفافة التفاعلية
    markup = InlineKeyboardMarkup(row_width=2)
    
    # الحصول على اسم البوت البرمجي لزر الإضافة المباشرة
    bot_info = bot.get_me()
    add_to_group_url = f"https://t.me/{bot_info.username}?startgroup=true"

    btn_add = InlineKeyboardButton("➕ أضف البوت لمجموعتك", url=add_to_group_url)
    btn_commands = InlineKeyboardButton("📜 قائمة الأوامر", callback_data="show_commands")
    btn_channel = InlineKeyboardButton("📢 القناة الرسمية", url="https://t.me/telegram") # يمكنك تغيير الرابط بقناتك
    btn_developer = InlineKeyboardButton("👑 المطور", callback_data="show_dev")

    # ترتيب الأزرار في صفوف
    markup.add(btn_add)
    markup.add(btn_commands, btn_channel)
    markup.add(btn_developer)

    bot.reply_to(message, caption, parse_mode="Markdown", reply_markup=markup)

# ----------------- معالجة الضغط على الأزرار الشفافة -----------------
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "show_commands":
        commands_text = (
            "🛠️ **قائمة أوامر حماية STAR BOT:**\n\n"
            "• `/mute` - لكتم العضو (بالرد على رسالته)\n"
            "• `/ban` - لحظر العضو من المجموعة (بالرد على رسالته)\n"
            "• `/pin` - لتثبيت الرسالة (بالرد على الرسالة)\n\n"
            "⚙️ *تأكد من إعطاء البوت كافة صلاحيات المشرف ليتمكن من التنفيذ.*"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, commands_text, parse_mode="Markdown")

    elif call.data == "show_dev":
        bot.answer_callback_query(call.id, text="المطور: STAR 🌟", show_alert=True)

# ----------------- أوامر الحظر والكتم والإدارة -----------------
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو الذي تريد كتمه.")
        return

    target_user = message.reply_to_message.from_user
    try:
        bot.restrict_chat_member(message.chat.id, target_user.id, until_date=0, can_send_messages=False)
        bot.reply_to(message, f"🚫 تم كتم العضو **{target_user.first_name}** بنجاح.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو الذي تريد حظره.")
        return

    target_user = message.reply_to_message.from_user
    try:
        bot.ban_chat_member(message.chat.id, target_user.id)
        bot.reply_to(message, f"🚷 تم حظر العضو **{target_user.first_name}** بنجاح.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

# ----------------- تشغيل البوت المستمر -----------------
if __name__ == '__main__':
    print("STAR BOT is running with a professional UI...")
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(3)
    
