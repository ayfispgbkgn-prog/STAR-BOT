import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# تنظيف الـ Webhook
try:
    bot.remove_webhook()
    print("STAR MUSIC BOT is starting...")
except Exception as e:
    print(f"Webhook Clean Warning: {e}")

# --- الواجهة الترحيبية ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_name = message.from_user.first_name
    caption = (
        f"🎧 <b>أهلاً بك يا {user_name} في STAR MUSIC!</b>\n\n"
        f"🎵 <b>أسرع بوت للبحث وتحميل الأغاني والصوتيات بجودة عالية.</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <b>طريقة الاستخدام:</b>\n"
        f"أرسل اسم الأغنية مباشرة أو استخدم الأمر:\n"
        f"<code>/play اسم الأغنية</code>\n"
        f"مثال: <code>فيروز كيفك انت</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 <b>أرسل اسم الأغنية الآن للبدء!</b>"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👑 المطور", callback_data="dev_info"))
    
    bot.reply_to(message, caption, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "dev_info")
def dev_callback(call):
    bot.answer_callback_query(call.id, text="تطوير: STAR 🌟", show_alert=True)

# --- دالة البحث والتنزيل السريعة ---
def download_and_send(chat_id, message_id, query):
    wait_msg = bot.send_message(chat_id, f"🔍 <b>جاري البحث عن:</b> <i>{query}</i> ...", parse_mode="HTML", reply_to_message_id=message_id)

    # إعدادات تنزيل محسّنة للسرعة والجودة
    ydl_opts = {
        'format': 'ba/ba*',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # تجربة يوتيوب ثم SoundCloud كبديل تلقائي
            try:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            except Exception:
                info = ydl.extract_info(f"scsearch1:{query}", download=True)

            if 'entries' in info and len(info['entries']) > 0:
                video_info = info['entries'][0]
            else:
                video_info = info

            title = video_info.get('title', 'Audio Track')
            duration = video_info.get('duration', 0)
            file_id = video_info.get('id')
            ext = video_info.get('ext', 'm4a')
            filepath = f"downloads/{file_id}.{ext}"

        if os.path.exists(filepath):
            bot.edit_message_text("🚀 <b>جاري رفع الملف الصوتي...</b>", chat_id=chat_id, message_id=wait_msg.message_id, parse_mode="HTML")
            
            with open(filepath, 'rb') as audio:
                bot.send_audio(
                    chat_id=chat_id,
                    audio=audio,
                    title=title,
                    performer="STAR MUSIC 🎵",
                    duration=duration,
                    reply_to_message_id=message_id
                )
            
            # تنظيف الملف فوراً
            os.remove(filepath)
            bot.delete_message(chat_id=chat_id, message_id=wait_msg.message_id)
        else:
            bot.edit_message_text("❌ تعذر العثور على مقطع مطابق، جرب كتابة اسم المطرب مع الأغنية.", chat_id=chat_id, message_id=wait_msg.message_id)

    except Exception as e:
        print(f"Music Error: {e}")
        bot.edit_message_text("❌ <b>حدث خطأ أثناء التنزيل.</b>\nتأكد من كتابة اسم الأغنية بشكل صحيح.", chat_id=chat_id, message_id=wait_msg.message_id, parse_mode="HTML")
        
        # تنظيف مجلد التنزيلات عند الأخطاء
        if os.path.exists('downloads'):
            for f in os.listdir('downloads'):
                os.remove(os.path.join('downloads', f))

# --- الاستجابة للأوامر والرسائل المباشرة ---
@bot.message_handler(commands=['play', 'song', 'يوت'])
def handle_play_cmd(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ <b>يرجى كتابة اسم الأغنية!</b>\nمثال: <code>/play فيروز</code>", parse_mode="HTML")
        return
    download_and_send(message.chat.id, message.message_id, args[1])

# البحث المباشر بدون الحاجة لأمر (فقط كتابة الاسم)
@bot.message_handler(func=lambda m: m.content_type == 'text' and not m.text.startswith('/'))
def handle_direct_search(message):
    download_and_send(message.chat.id, message.message_id, message.text)

# --- تشغيل البوت ---
if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    print("STAR MUSIC BOT is Live!")
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=30, skip_pending=True)
        except Exception as e:
            time.sleep(5)
            
