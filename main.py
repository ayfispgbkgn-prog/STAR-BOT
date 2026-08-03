import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import time
import os
import yt_dlp
from config import TOKEN

# إنشاء كائن البوت
bot = telebot.TeleBot(TOKEN)

# تنظيف الـ Webhook عند بدء التشغيل
try:
    bot.remove_webhook()
    print("STAR BOT: Webhook cleaned successfully.")
except Exception as e:
    print(f"STAR BOT: Webhook warning: {e}")

# دالة التحقق من صلاحيات المشرفين
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception:
        return False

# ==========================================
# 1️⃣ الواجهة الترحيبية والأزرار الشفافة
# ==========================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    caption = (
        f"⚡ <b>أهلاً بك يا {user_name} في بوت STAR!</b>\n\n\
        > هو النظام الأقوى لإدارة وحماية المجموعات .\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ <b>المميزات المتاحة:</b>\n"
        f"└ 🚷 <b>أوامر الكتم والحظر والإبعاد</b>\n"
        f"└ 📌 <b>تثبيت الرسائل وإدارتها</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 <b>قم بإضافة البوت لمجموعتك ورَفّعه مشرفاً للبدء!</b>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    try:
        bot_info = bot.get_me()
        add_to_group_url = f"https://t.me/{bot_info.username}?startgroup=true"
    except Exception:
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
            "🛠️ <b>قائمة أوامر STAR BOT:</b>\n\n"
            "🎵 <b>أوامر الموسيقى:</b>\n"
            "• <code>/يوت اسم الأغنية</code> - للبحث عن أغنية وتحميلها بصيغة صوتية.\n\n"
            "🛡️ <b>أوامر الإدارة والتنظيف:</b>\n"
            "• <code>/mute</code> - لكتم عضو (بالرد على رسالته)\n"
            "• <code>/unmute</code> - لفك كتم عضو (بالرد على رسالته)\n"
            "• <code>/kick</code> - لطرد عضو من المجموعة (بالرد على رسالته)\n"
            "• <code>/ban</code> - لحظر عضو نهائياً (بالرد على رسالته)\n"
            "• <code>/unban</code> - لفك حظر عضو (بالرد على رسالته)\n"
            "• <code>/pin</code> - لتثبيت الرسالة (بالرد عليها)"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, commands_text, parse_mode="HTML")

    elif call.data == "show_dev":
        bot.answer_callback_query(call.id, text="المطور: STAR 🌟", show_alert=True)

# ==========================================
# 3️⃣ أوامر الحماية والإدارة (Moderation)
# ==========================================

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "⚠️ هذا الأمر يعمل داخل المجموعات فقط!")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو الذي تريد كتمه.")
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
        bot.restrict_chat_member(message.chat.id, target_user.id, permissions=no_send_permissions)
        bot.reply_to(message, f"🚫 تم كتم العضو <b>{target_user.first_name}</b> بنجاح.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء الكتم: <code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "⚠️ هذا الأمر يعمل داخل المجموعات فقط!")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو المراد فك كتمه.")
        return

    target_user = message.reply_to_message.from_user

    try:
        full_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        bot.restrict_chat_member(message.chat.id, target_user.id, permissions=full_permissions)
        bot.reply_to(message, f"🔊 تم فك الكتم عن العضو <b>{target_user.first_name}</b> بنجاح.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء فك الكتم: <code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "⚠️ هذا الأمر يعمل داخل المجموعات فقط!")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو الذي تريد طرده.")
        return

    target_user = message.reply_to_message.from_user

    if is_admin(message.chat.id, target_user.id):
        bot.reply_to(message, "⚠️ لا يمكنك طرد مشرف أو مالك المجموعة!")
        return

    try:
        bot.ban_chat_member(message.chat.id, target_user.id)
        bot.unban_chat_member(message.chat.id, target_user.id)
        bot.reply_to(message, f"👞 تم طرد العضو <b>{target_user.first_name}</b> من المجموعة.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ تعذر طرد العضو: <code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "⚠️ هذا الأمر يعمل داخل المجموعات فقط!")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو الذي تريد حظره.")
        return

    target_user = message.reply_to_message.from_user

    if is_admin(message.chat.id, target_user.id):
        bot.reply_to(message, "⚠️ لا يمكنك حظر مشرف أو مالك المجموعة!")
        return

    try:
        bot.ban_chat_member(message.chat.id, target_user.id)
        bot.reply_to(message, f"🚷 تم حظر العضو <b>{target_user.first_name}</b> نهائياً من المجموعة.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ تعذر حظر العضو: <code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "⚠️ هذا الأمر يعمل داخل المجموعات فقط!")
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على رسالة العضو المراد فك حظره.")
        return

    target_user = message.reply_to_message.from_user

    try:
        bot.unban_chat_member(message.chat.id, target_user.id)
        bot.reply_to(message, f"✅ تم فك الحظر عن <b>{target_user.first_name}</b>. يمكنه الانضمام الآن.", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ تعذر فك الحظر: <code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['pin'])
def pin_message(message):
    if message.chat.type not in ['group', 'supergroup']:
        return

    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر مخصص للمشرفين فقط!")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ قم بالرد على الرسالة التي تريد تثبيتها.")
        return

    try:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message, "📌 تم تثبيت الرسالة بنجاح!")
    except Exception as e:
        bot.reply_to(message, f"❌ تعذر تثبيت الرسالة: <code>{e}</code>", parse_mode="HTML")

# ==========================================
# 4️⃣ الحلقة المباشرة لتشغيل البوت
# ==========================================

if __name__ == '__main__':
    print("STAR BOT is active with Music & Protection modules...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=30, skip_pending=True)
        except Exception as e:
            print(f"Polling error encountered: {e}")
            time.sleep(5)
        
