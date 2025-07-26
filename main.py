import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Token do Bot
BOT_TOKEN = "COLE_SEU_TOKEN_AQUI"

# URL da planilha
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"

# Conectar à planilha Google Sheets
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

# Mensagem de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
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
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

# Botões do menu
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'investir':
        await query.edit_message_text("💵 *Digite o valor que pretende investir (ex.: 500 USD)*", parse_mode="Markdown")
        context.user_data['esperando_valor'] = True

    elif query.data == 'pt':
        await query.edit_message_text("✅ *Como comprar (PT)*\n\n1️⃣ Envie BNB para a carteira...\n2️⃣ Após confirmação, o token será enviado automaticamente.", parse_mode="Markdown")

    elif query.data == 'en':
        await query.edit_message_text("🌍 *How to buy (EN)*\n\n1️⃣ Send BNB to the wallet...\n2️⃣ After confirmation, the token will be sent automatically.", parse_mode="Markdown")

    elif query.data == 'status':
        await query.edit_message_text("📊 *Status da pré-venda*\n\n🔥 Restam poucas unidades com preço promocional!", parse_mode="Markdown")

    elif query.data == 'outros':
        await query.edit_message_text("📌 *Temos outras oportunidades de investimento!*\nEm breve enviaremos mais detalhes.", parse_mode="Markdown")

# Registrar o valor que o usuário digitar
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        user = update.message.from_user
        sheet = conectar_planilha()
        sheet.append_row([
            user.full_name,
            f"@{user.username}" if user.username else "Sem username",
            valor,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ])
        await update.message.reply_text(f"✅ Investimento *{valor}* registrado com sucesso!", parse_mode="Markdown")
        context.user_data['esperando_valor'] = False

# Inicializar o Bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT ONLINE com boas-vindas automáticas e integração ao Google Sheets!")
    app.run_polling()

if __name__ == "__main__":
    main()
