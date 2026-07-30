import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ STAR BOT يعمل بنجاح!")

def main():
    # بناء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start))
    
    print("STAR BOT is running...")
    
    # تشغيل البوت بالطريقة الرسمية والمستقرة
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
