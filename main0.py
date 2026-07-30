from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from config import TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ STAR BOT يعمل بنجاح!\n\n"
        "مرحبًا بك، هذه أول نسخة من البوت."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("STAR BOT is running...")

    app.run_polling()


if __name__ == "__main__":
    main()