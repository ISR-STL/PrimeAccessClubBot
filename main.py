from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "SEU_TOKEN_AQUI"

# Link do Google Forms
FORM_LINK = "https://forms.gle/zVJN3BBuZgzCcGB36"

# Mensagem principal
message_pt = f"""
🚀 *Pré-venda SoByen (SBN)*

✅ Preço pré-venda: **US$ 0,01**
✅ Lucro imediato: **+100%**
✅ Pagamento via **BNB (Rede BSC)**

📌 **Quer prioridade antes que acabe?**
👉 [Clique aqui para entrar na Whitelist]({FORM_LINK})
"""

status_msg = """
📊 **Status da Pré-venda SBN**
✅ Preço atual: **US$ 0,01**
✅ Próximo preço: **US$ 0,02**
✅ Duração: Apenas **48h**
✅ Vagas whitelist: **500 primeiras pessoas**
⏳ Restante: **tempo limitado**
"""

# Comando inicial com botões
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')],
        [InlineKeyboardButton("💼 Ver outras ofertas", callback_data='offers')],
        [InlineKeyboardButton("💰 Informar valor que deseja investir", callback_data='invest')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✅ Bot ativo! Escolha uma opção abaixo:",
        reply_markup=reply_markup
    )

# Resposta aos botões
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pt':
        await query.edit_message_text(
            text=message_pt,
            parse_mode="Markdown",
            disable_web_page_preview=True  # ✅ REMOVE o preview poluído
        )
    elif query.data == 'status':
        await query.edit_message_text(
            text=status_msg,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    elif query.data == 'offers':
        await query.edit_message_text(
            "📌 *Temos outras oportunidades de investimento!*\nEm breve enviaremos mais detalhes.",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    elif query.data == 'invest':
        await query.edit_message_text(
            "💰 *Informe o valor que deseja investir e nossa equipe entrará em contato.*",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✅ BOT ONLINE - aguardando comandos...")
    app.run_polling()

if __name__ == "__main__":
    main()
