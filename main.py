import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
except Exception:
    pass

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
        f"👇 <b>قم بإضافة البوت لمجموعتك ورَفّعه مشرفاً للبدء!</b>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    try:
        bot_info = bot.get_me()
        add_to_group_url = f"https://t.me/{bot_info.username}?startgroup=true"
    except:
        add_to_group_url = "https://t.me/"

    btn_add = InlineKeyboardButton("➕ أضف البوت لمجموعتك", url=add_to_group_url)
    btn_commands = InlineKeyboardButton("📜 قائمة الأوامر", callback_data="show_commands")
    markup.add(btn_add, btn_commands)

    bot.reply_to(message, caption, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "show_commands":
        commands_text = (
            "🛠️ <b>قائمة أوامر حماية STAR BOT:</b>\n\n"
            "• <code>/mute</code> - لكتم عضو (بالرد على رسالته)\n"
            "• <code>/unmute</code> - لفك كتم عضو (بالرد على رسالته)"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, commands_text, parse_mode="HTML")

# ----------------- أمر الكتم المطور -----------------
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "⚠️ هذا الأمر يعمل داخل المجموعات فقط!")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    target_user_id = None
    target_name = ""

    # الحالة الأولى: إذا كان رداً على رسالة
    if message.reply_to_message:
        target_user_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
    else:
        # الحالة الثانية: إذا كتب المستخدم المعرف أو اليوزر بجانب الأمر مثل /mute @username
        args = message.text.split()
        if len(args) > 1:
            username = args[1].replace("@", "")
            try:
                # محاولة جلب معرف المستخدم من خلال اليوزر
                chat_member = bot.get_chat_member(message.chat.id, username)
                # ملاحظة: get_chat_member يتطلب معرف رقمي أو يوزر حسب المكتبة، سنعتمد على الطريقة الآمنة بالرد
            except Exception:
                pass

    if not target_user_id:
        bot.reply_to(message, "⚠️ **خطأ:** يجب عليك **الرد على رسالة العضو** الذي تريد كتمه بـ `/mute`", parse_mode="HTML")
        return

    if is_admin(message.chat.id, target_user_id):
        bot.reply_to(message, "⚠️ لا يمكنك كتم مشرف أو مالك المجموعة!")
        return

    try:
        no_send_permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
        
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user_id,
            permissions=no_send_permissions
        )
        bot.reply_to(message, f"🚫 تم كتم العضو <b>{target_name}</b> بنجاح.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n<code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو المراد فك كتمه.")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        return

    target_user_id = message.reply_to_message.from_user.id
    target_name = message.reply_to_message.from_user.first_name

    try:
        full_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user_id,
            permissions=full_permissions
        )
        bot.reply_to(message, f"🔊 تم فك الكتم عن العضو <b>{target_name}</b> بنجاح.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: <code>{e}</code>", parse_mode="HTML")

if __name__ == '__main__':
    print("STAR BOT is active...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=30, skip_pending=True)
        except Exception as e:
            time.sleep(5)
                     
