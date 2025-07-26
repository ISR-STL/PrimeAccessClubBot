from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from googletrans import Translator

BOT_TOKEN = "SEU_TOKEN_AQUI"

translator = Translator()

# Função segura para traduzir (evita travar se a API falhar)
def safe_translate(text, dest='en'):
    try:
        result = translator.translate(text, dest=dest)
        return result.text
    except Exception as e:
        print(f"⚠ Erro na tradução: {e}")
        return text  # fallback para o texto original

# Mensagens base (em português)
message_pt = """
🚨 PRÉ-VENDA EXPRESS DO TOKEN SOBYEN (SBN) – 48H! 🚨

✅ Pré-venda: US$ 0,01  
✅ Listagem PancakeSwap: US$ 0,02 (lucro imediato 100%)  
✅ Compra mínima: US$ 5 | Máxima: US$ 1.000  
✅ Pagamento: BNB (Rede BSC)

💳 Carteira oficial:
0x0d5B9634F1C33684C9d2606109B391301b95f002

⏳ Apenas 48h! Liquidez travada 12 meses
👉 [Preencher Whitelist](https://forms.gle/zVJN3BBuZgzCcGB36)
"""

status_msg = """
📊 STATUS DA PRÉ-VENDA
✅ Preço atual: **US$ 0,01**
✅ Próximo preço: **US$ 0,02**
✅ Duração: Apenas **48h**
✅ Vagas whitelist: **500 primeiras pessoas**
⏳ Restante: **tempo limitado**
"""

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (Auto)", callback_data='auto')],
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
        await query.edit_message_text(text=message_pt)
    elif query.data == 'auto':
        user_lang = query.from_user.language_code or 'en'
        translated = safe_translate(message_pt, dest=user_lang)
        await query.edit_message_text(text=translated)
    elif query.data == 'status':
        await query.edit_message_text(text=status_msg)
    elif query.data == 'offers':
        await query.edit_message_text("📌 Temos outras oportunidades de investimento! Em breve enviaremos mais detalhes.")
    elif query.data == 'invest':
        await query.edit_message_text("💰 Digite o valor que você deseja investir e nossa equipe entrará em contato!")

# Função principal
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✅ BOT ONLINE - aguardando comandos…")
    app.run_polling()

if __name__ == "__main__":
    main()
