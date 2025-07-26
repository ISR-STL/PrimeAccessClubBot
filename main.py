import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ✅ TOKEN DO NOVO BOT
BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"

# ✅ MENSAGENS SIMPLIFICADAS
message_pt = "✅ Pré-venda SBN ativa! Preço atual: US$ 0,01. Próximo preço: US$ 0,02.\nWhitelist: https://forms.gle/5sJNUBMTusfRfxqSA"
message_en = "✅ SBN Pre-sale active! Current price: US$ 0.01. Next price: US$ 0.02.\nWhitelist: https://forms.gle/5sJNUBMTusfRfxqSA"
status_msg = "📊 Status: 48h restantes. Liquidez travada 12 meses. Apenas 500 vagas whitelist."

# ✅ HANDLER DO /START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✅ Bot ativo! Escolha uma opção:", reply_markup=reply_markup)

# ✅ BOTÕES INLINE
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'pt':
        await query.edit_message_text(text=message_pt)
    elif query.data == 'en':
        await query.edit_message_text(text=message_en)
    elif query.data == 'status':
        await query.edit_message_text(text=status_msg)

# ✅ FUNÇÃO QUE RODA O BOT EM THREAD SEPARADA
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("🤖 BOT INICIADO E RODANDO EM POLLING...")
    app.run_polling()

# ✅ FLASK PARA HEALTHCHECK
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Bot está rodando no Railway!"

# ✅ INICIALIZADOR
if __name__ == "__main__":
    # Rodar bot em thread paralela
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Rodar flask para manter Railway ativo
    flask_app.run(host="0.0.0.0", port=8080)
