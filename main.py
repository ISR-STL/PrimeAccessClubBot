from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token do novo bot
BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"

# Comando básico de teste
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /start RECEBIDO!")  # Vai aparecer no log do Railway
    await update.message.reply_text("✅ Bot novo está online e respondendo corretamente!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 BOT NOVO ONLINE - AGUARDANDO COMANDOS")
    app.run_polling()

if __name__ == "__main__":
    main()
