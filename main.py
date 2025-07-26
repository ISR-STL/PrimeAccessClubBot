from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# Ativar logs para ver no Railway
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"

FORMS_LINK = "https://forms.gle/5sJNUBMTusfRfxqSA"

message_pt = f"""
🚨 **PRÉ-VENDA EXPRESS – SOMENTE 48 HORAS!** 🚨

🔥 SoByen (SBN) – Token do agronegócio digital com escassez programada  

✅ Pré-venda: US$ 0,01  
✅ Listagem: US$ 0,02 (lucro imediato 100%)  
✅ Compra mínima: US$ 5 | Máxima: US$ 1.000  
✅ Pagamento: BNB (Rede BSC)

💳 **Carteira oficial:**  
`0x0d5B9634F1C33684C9d2606109B391301b95f002`

⏳ Apenas 48h! Liquidez travada 12 meses  
👉 **Whitelist (limitada aos 500 primeiros):**  
[{FORMS_LINK}]({FORMS_LINK})
"""

status_msg = """
📊 **Status da Pré-venda SBN**
✅ Preço atual: **US$ 0,01**
✅ Próximo preço: **US$ 0,02**
✅ Duração: Apenas **48h**
✅ Vagas whitelist: **500 primeiras pessoas**
⏳ Restante: **tempo limitado**
"""

outras_ofertas_msg = """
💼 **Outras oportunidades AgroDigital**  

✅ Tokens de novos projetos  
✅ Pré-vendas exclusivas com bônus  
✅ Investimentos em ecossistema sustentável  

Se tiver interesse, clique no botão *Quero investir* e informe o valor que pretende alocar.
"""

# Estado para armazenar quem está respondendo o valor
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/start recebido de {update.effective_user.username}")

    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')],
        [InlineKeyboardButton("📝 Entrar na Whitelist", url=FORMS_LINK)],
        [InlineKeyboardButton("💼 Outras ofertas", callback_data='ofertas')],
        [InlineKeyboardButton("💰 Quero investir", callback_data='investir')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✅ *AgroDigital Bot ativo!* Escolha uma opção abaixo:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pt':
        await query.edit_message_text(text=message_pt, parse_mode="Markdown")
    elif query.data == 'en':
        await query.edit_message_text(text="🌍 *Soon in English!*", parse_mode="Markdown")
    elif query.data == 'status':
        await query.edit_message_text(text=status_msg, parse_mode="Markdown")
    elif query.data == 'ofertas':
        await query.edit_message_text(text=outras_ofertas_msg, parse_mode="Markdown")
    elif query.data == 'investir':
        # Muda o estado do usuário para coletar valor
        user_state[query.from_user.id] = "waiting_investment"
        await query.message.reply_text("💰 *Qual valor você pretende investir?* (ex: 100, 500, 1000 USD)")

async def coletar_valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_state.get(user_id) == "waiting_investment":
        valor = update.message.text
        logger.info(f"Usuário {update.effective_user.username} quer investir: {valor}")
        await update.message.reply_text(f"✅ Recebemos sua intenção de investir *US$ {valor}*! Nossa equipe entrará em contato.")
        # Depois de coletar o valor, reseta o estado
        user_state.pop(user_id)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, coletar_valor))  # captura valores

    logger.info("🤖 BOT ONLINE - aguardando comandos...")
    app.run_polling()

if __name__ == "__main__":
    main()
