import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = "SEU_TOKEN_AQUI"

# URL da planilha
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"

# Conectar com Google Sheets
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

# Função para mostrar o menu principal
def menu_principal():
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')],
        [InlineKeyboardButton("💼 Ver outras ofertas", callback_data='outros')],
        [InlineKeyboardButton("💰 Informar valor que deseja investir", callback_data='investir')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Função de boas-vindas
async def mensagem_boas_vindas(chat_id, context: ContextTypes.DEFAULT_TYPE):
    texto_boas_vindas = (
        "👋 *Bem-vindo(a) ao AgroDigital Club!*\n\n"
        "🌱 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial de crescimento global.\n\n"
        "💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\n"
        "Escolha uma opção abaixo para continuar 👇"
    )
    await context.bot.send_message(chat_id=chat_id, text=texto_boas_vindas, reply_markup=menu_principal(), parse_mode="Markdown")

# Handler do comando /start (continua funcionando)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mensagem_boas_vindas(update.effective_chat.id, context)

# Handler automático quando o usuário inicia o chat pela primeira vez
async def novo_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member:
        status_novo = update.my_chat_member.new_chat_member.status
        if status_novo == "member":  # usuário iniciou o chat
            await mensagem_boas_vindas(update.effective_chat.id, context)

# Callback dos botões
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'investir':
        await query.edit_message_text("💵 *Digite o valor que pretende investir (ex.: 500 USD)*", parse_mode="Markdown")
        context.user_data['esperando_valor'] = True

# Captura o valor informado e registra no Sheets
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

# Inicialização do BOT
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comando /start
    app.add_handler(CommandHandler("start", start))

    # Detecta novo chat sem precisar de /start
    app.add_handler(ChatMemberHandler(novo_chat, ChatMemberHandler.MY_CHAT_MEMBER))

    # Botões
    app.add_handler(CallbackQueryHandler(button_callback))

    # Mensagens normais para registrar investimento
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))

    print("✅ BOT ONLINE com boas-vindas automáticas e integração ao Google Sheets!")
    app.run_polling()

if __name__ == "__main__":
    main()
