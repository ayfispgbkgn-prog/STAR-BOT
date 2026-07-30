ℕ | I ʟυͷσ‌‎xᴀ:
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
    print("Webhook removed successfully.")
except Exception as e:
    print(f"Error removing webhook: {e}")

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception:
        return False

# ----------------- الواجهة الترحيبية -----------------
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
    try:
        bot_info = bot.get_me()
        add_to_group_url = f"https://t.me/{bot_info.username}?startgroup=true"
    except:
        add_to_group_url = "https://t.me/"

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
            "• <code>/mute</code> - لكتم عضو (بالرد على رسالته)\n"
            "• <code>/unmute</code> - لفك كتم عضو (بالرد على رسالته)\n"
            "• <code>/ban</code> - لحظر عضو (بالرد على رسالته)"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, commands_text, parse_mode="HTML")
    elif call.data == "show_dev":
        bot.answer_callback_query(call.id, text="المطور: STAR 🌟", show_alert=True)

# ----------------- أمر الكتم المحدث -----------------
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو الذي تريد كتمه.")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    target_user = message.reply_to_message.from_user

    if is_admin(message.chat.id, target_user.id):
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
            user_id=target_user.id,
            permissions=no_send_permissions
        )
        bot.reply_to(message, f"🚫 تم كتم العضو <b>{target_user.first_name}</b> بنجاح.", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ عند الكتم:\n<code>{e}</code>\n\n💡 تأكد أن المجموعة خارقة (Supergroup) وأن البوت يمتلك صلاحية حظر المستخدمين.", parse_mode="HTML")

# ----------------- أمر فك الكتم -----------------
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو المراد فك كتمه.")
        return

if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    target_user = message.reply_to_message.from_user

    try:
        full_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            permissions=full_permissions
        )
        bot.reply_to(message, f"🔊 تم فك الكتم عن العضو <b>{target_user.first_name}</b> بنجاح.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: <code>{e}</code>", parse_mode="HTML")

# ----------------- تشغيل البوت -----------------
if name == 'main':
    print("STAR BOT is active...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=30, skip_pending=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
Open your script in Pydroid 3
Tap the Run (▶️) button
Look at the console/output panel at the bottom — it'll show either:
STAR BOT is active... (meaning it started fine)
A red error/traceback (meaning it crashed on startup)
Nothing at all (meaning it might be stuck or Pydroid lost the process)
