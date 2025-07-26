import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ✅ NOVO TOKEN DO BOT
BOT_TOKEN = "8046727069:AAHTosHwoA0BIRDTwj-zk48k6RqfxiRysP8"

# ✅ URL DA PLANILHA
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"

# ✅ Conectar à planilha
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

# ✅ Mensagem de boas-vindas automática
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem_boas_vindas = (
        "👋 *Bem-vindo(a) ao AgroDigital Club!*\n\n"
        "🌱 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial de crescimento global.\n\n"
        "💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\n"
        "Escolha uma opção abaixo para continuar 👇"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')],
        [InlineKeyboardButton("💼 Ver outras ofertas", callback_data='outros')],
        [InlineKeyboardButton("💰 Informar valor que deseja investir", callback_data='investir')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(mensagem_boas_vindas, reply_markup=reply_markup, parse_mode="Markdown")

# ✅ Quando usuário clica em algum botão
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'investir':
        await query.edit_message_text(
            "💵 *Digite o valor que pretende investir (ex.: 500 USD)*\n\n"
            "_Você pode editar o valor acima das nossas propostas para personalizar o investimento._",
            parse_mode="Markdown"
        )
        context.user_data['esperando_valor'] = True

# ✅ Registrar investimento na planilha
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        user = update.message.from_user

        # Salva na planilha
        sheet = conectar_planilha()
        sheet.append_row([
            user.full_name,
            f"@{user.username}" if user.username else "Sem username",
            valor,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ])

        await update.message.reply_text(f"✅ Investimento *{valor}* registrado com sucesso!", parse_mode="Markdown")
        context.user_data['esperando_valor'] = False

# ✅ Iniciar o bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers principais
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))

    print("✅ BOT ONLINE com mensagem de boas-vindas + botões + integração ao Google Sheets!")
    app.run_polling()

if __name__ == "__main__":
    main()
