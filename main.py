import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Pega variáveis do Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")

# Monta URL do webhook
WEBHOOK_URL = f"https://{RAILWAY_PUBLIC_DOMAIN}/{BOT_TOKEN}"

# Mensagens
message_pt = """
🚨 PRÉ-VENDA EXPRESS – SOMENTE 48 HORAS! 🚨

🔥 SoByen (SBN) – Token do agronegócio digital com escassez programada  

✅ Pré-venda: US$ 0,01  
✅ Listagem: US$ 0,02 (lucro imediato 100%)  
✅ Compra mínima: US$ 5 | Máxima: US$ 1.000  
✅ Pagamento: BNB (Rede BSC)

💳 Carteira oficial:
0x0d5B9634F1C33684C9d2606109B391301b95f002

⏳ Apenas 48h! Liquidez travada 12 meses
👉 Whitelist (limitada aos 500 primeiros):
https://forms.gle/5sJNUBMTusfRfxqSA
"""

message_en = """
🚨 FLASH PRE-SALE – ONLY 48 HOURS! 🚨

🔥 SoByen (SBN) – The digital agribusiness token with programmed scarcity  

✅ Pre-sale: US$ 0.01  
✅ Listing: US$ 0.02 (instant 100% profit)  
✅ Min: US$ 5 | Max: US$ 1,000  
✅ Payment: BNB (BSC Network)

💳 Official wallet:
0x0d5B9634F1C33684C9d2606109B391301b95f002

⏳ Only 48h! Liquidity locked for 12 months
👉 Whitelist (limited to first 500 users):
https://forms.gle/5sJNUBMTusfRfxqSA
"""

status_msg = """
📊 **Status da Pré-venda SBN**
✅ Preço atual: **US$ 0,01**
✅ Próximo preço: **US$ 0,02**
✅ Duração: Apenas **48h**
✅ Vagas whitelist: **500 primeiras pessoas**
⏳ Restante: **tempo limitado**
"""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✅ Bot ativo! Escolha uma opção abaixo:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pt':
        await query.edit_message_text(text=message_pt)
    elif query.data == 'en':
        await query.edit_message_text(text=message_en)
    elif query.data == 'status':
        await query.edit_message_text(text=status_msg)

# Flask para manter Railway ativo
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Bot está rodando no Railway!"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Adiciona handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Configura webhook
    app.bot.set_webhook(WEBHOOK_URL)

    # Inicia Flask para manter vivo
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
