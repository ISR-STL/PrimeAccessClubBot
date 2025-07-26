from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start recebido!")
    await update.message.reply_text("✅ Bot está ativo e respondendo normalmente!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 BOT ONLINE – aguardando comandos…")
    app.run_polling()

if __name__ == "__main__":
    main()
