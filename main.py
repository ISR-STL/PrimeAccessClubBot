from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from googletrans import Translator  # Tradução automática

# Token do Bot
BOT_TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo token correto

# Instância do tradutor
translator = Translator()

# Mensagens principais
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
👉 Whitelist:
https://forms.gle/zVJN3BBuZgzCcGB36
"""

status_msg = """
📊 **Status da Pré-venda SBN**
✅ Preço atual: **US$ 0,01**
✅ Próximo preço: **US$ 0,02**
✅ Duração: Apenas **48h**
✅ Vagas whitelist: **500 primeiras pessoas**
⏳ Restante: **tempo limitado**
"""

# Função de tradução automática
def traduzir_texto(texto, idioma_destino):
    traducao = translator.translate(texto, dest=idioma_destino)
    return traducao.text

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

# Callback dos botões
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pt':
        await query.edit_message_text(text=message_pt)

    elif query.data == 'en':
        # Traduz automaticamente para inglês
        msg_en = traduzir_texto(message_pt, 'en')
        await query.edit_message_text(text=msg_en)

    elif query.data == 'status':
        await query.edit_message_text(text=status_msg)

    elif query.data == 'offers':
        await query.edit_message_text(
            "📌 Temos outras oportunidades de investimento!\nEm breve enviaremos mais detalhes."
        )

    elif query.data == 'invest':
        await query.edit_message_text(
            "💰 Informe o valor que deseja investir e entraremos em contato!"
        )

# Função principal
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✅ BOT ONLINE – aguardando comandos...")
    app.run_polling()

if __name__ == "__main__":
    main()
