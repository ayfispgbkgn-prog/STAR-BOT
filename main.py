import asyncio
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

async def main():
    # بناء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("STAR BOT is running...")
    
    # تشغيل الـ Polling بطريقة يدويّة تتفادى مشكلة Event Loop في Render
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # إبقاء البوت متصلاً
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    
