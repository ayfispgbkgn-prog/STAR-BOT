from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8647401064:AAGWowezYXit9BI8lAu7M-N4yoTX7dcXlQA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ أهلاً بك في STAR BOT")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 الأوامر:\n/start\n/help")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("🤖 STAR BOT يعمل...")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()