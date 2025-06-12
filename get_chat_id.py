from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Твій chat_id: {chat_id}")

if __name__ == "__main__":
    app = ApplicationBuilder().token("8018888910:AAGQlpp-t0Z6LiVxTQ9Sa8C9YDhRW5rmkVo").build()

    app.add_handler(CommandHandler("start", start))

    print("Бот запущений, надішли /start своєму боту в Telegram")
    app.run_polling()
