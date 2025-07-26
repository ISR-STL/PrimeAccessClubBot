from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Token do novo bot
BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"

# Mensagens básicas
msg_boas_vindas = "✅ Bot ativo! Escolha uma opção abaixo:"
msg_pt = (
    "🚀 *Pré-venda SoByen (SBN)*\n\n"
    "✅ Preço atual: *US$ 0,01*\n"
    "✅ Próximo preço: *US$ 0,02*\n"
    "✅ Pagamento: BNB (BSC Network)\n\n"
    "💳 *Carteira oficial:*\n"
    "`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n"
    "👉 *Whitelist (limitada aos 500 primeiros):*\n"
    "[Cadastro Google Forms](https://forms.gle/5sJNUBMTusfRfxqSA)"
)
msg_en = (
    "🚀 *Pre-sale SoByen (SBN)*\n\n"
    "✅ Current price: *US$ 0.01*\n"
    "✅ Next price: *US$ 0.02*\n"
    "✅ Payment: BNB (BSC Network)\n\n"
    "💳 *Official wallet:*\n"
    "`0x0d5B9634F1C33684C9d2606109B391301b95f002`\n\n"
    "👉 *Whitelist (limited to the first 500 users):*\n"
    "[Google Forms Registration](https://forms.gle/5sJNUBMTusfRfxqSA)"
)
msg_status = (
    "📊 *Status da Pré-venda SBN*\n"
    "✅ Preço atual: *US$ 0,01*\n"
    "✅ Próximo preço: *US$ 0,02*\n"
    "✅ Duração: Apenas *48h*\n"
    "✅ Vagas whitelist: *500 primeiras pessoas*\n"
    "⏳ Restante: *tempo limitado*"
)
msg_outros = "📌 *Temos outras oportunidades de investimento!*\nEm breve enviaremos mais detalhes."

# Função de start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')],
        [InlineKeyboardButton("💼 Ver outras ofertas", callback_data='outros')],
        [InlineKeyboardButton("💰 Informar valor que deseja investir", callback_data='investir')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg_boas_vindas, reply_markup=reply_markup)

# Resposta aos botões
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pt':
        await query.edit_message_text(text=msg_pt, parse_mode="Markdown")
    elif query.data == 'en':
        await query.edit_message_text(text=msg_en, parse_mode="Markdown")
    elif query.data == 'status':
        await query.edit_message_text(text=msg_status, parse_mode="Markdown")
    elif query.data == 'outros':
        await query.edit_message_text(text=msg_outros, parse_mode="Markdown")
    elif query.data == 'investir':
        await query.edit_message_text(
            text="💵 *Qual valor pretende investir?*\nDigite no chat e nossa equipe entrará em contato!",
            parse_mode="Markdown"
        )

# Função principal
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ BOT ONLINE - aguardando comandos...")
    app.run_polling()

if __name__ == "__main__":
    main()
