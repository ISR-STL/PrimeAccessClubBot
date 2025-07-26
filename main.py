import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==================== CONFIGURAÇÕES PRINCIPAIS ====================
BOT_TOKEN = "8046727069:AAHTosHwoA0BIRDTwj-zk48k6RqfxiRysP8"
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"
GOOGLE_FORMS_URL = "https://forms.gle/zVJN3BBuZgzCcGB36"

# ==================== CONEXÃO GOOGLE SHEETS =======================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(PLANILHA_URL).sheet1
    return sheet

def registrar_acao(user, idioma, acao, valor="--"):
    try:
        sheet = conectar_planilha()
        sheet.append_row([
            user.full_name,
            f"@{user.username}" if user.username else "Sem username",
            idioma,
            acao,
            valor,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ])
    except Exception as e:
        print(f"Erro ao registrar na planilha: {e}")

# ==================== MENSAGENS POR IDIOMA ========================
mensagens = {
    "pt": {
        "bemvindo": "🌱 Bem-vindo(a) ao *AgroDigital Club*!\n\n🚀 Aqui você encontra oportunidades exclusivas no agronegócio digital com potencial de crescimento global.\n\n💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\nEscolha uma opção abaixo para continuar 👇",
        "botoes": [
            ("✅ Como comprar", "comprar"),
            ("📄 Abrir formulário", "formulario"),
            ("💰 Informar valor que deseja investir", "investir")
        ]
    },
    "en": {
        "bemvindo": "🌍 Welcome to *AgroDigital Club*!\n\n🚀 Here you will find exclusive opportunities in digital agribusiness with global growth potential.\n\n💡 *Join the pre-sale of the SoByen (SBN) token and secure your strategic position in the market.*\n\nChoose an option below 👇",
        "botoes": [
            ("🌍 How to buy", "comprar"),
            ("📄 Open whitelist form", "formulario"),
            ("💰 Enter the amount you want to invest", "investir")
        ]
    },
    "es": {
        "bemvindo": "🌾 ¡Bienvenido(a) a *AgroDigital Club*!\n\n🚀 Aquí encontrará oportunidades exclusivas en el agronegocio digital con potencial de crecimiento global.\n\n💡 *Participe en la preventa del token SoByen (SBN) y asegure una posición estratégica en el mercado.*\n\nSeleccione una opción abajo 👇",
        "botoes": [
            ("✅ Cómo comprar", "comprar"),
            ("📄 Abrir formulario", "formulario"),
            ("💰 Ingresar el monto que desea invertir", "investir")
        ]
    }
}

# ==================== START - ESCOLHA IDIOMA ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌍 *Choose your language / Escolha seu idioma / Elige tu idioma:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ==================== APÓS ESCOLHER IDIOMA ========================
async def escolher_idioma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = query.data.split("_")[1]  # en, pt, es
    context.user_data["idioma"] = idioma

    # Registrar que o usuário entrou e escolheu idioma
    registrar_acao(query.from_user, idioma, "Escolheu idioma")

    msg = mensagens[idioma]["bemvindo"]
    botoes = mensagens[idioma]["botoes"]
    keyboard = [[InlineKeyboardButton(txt, callback_data=data)] for txt, data in botoes]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

# ==================== BOTÕES PRINCIPAIS ===========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idioma = context.user_data.get("idioma", "en")  # Default inglês

    if query.data == "formulario":
        registrar_acao(query.from_user, idioma, "Abriu Formulário")
        await query.edit_message_text(
            f"📄 *O formulário será aberto em inglês para padronização global.*\n\n{GOOGLE_FORMS_URL}",
            parse_mode="Markdown"
        )
    elif query.data == "investir":
        await query.edit_message_text("💵 *Digite o valor que pretende investir (ex.: 500 USD)*", parse_mode="Markdown")
        context.user_data['esperando_valor'] = True
    elif query.data == "comprar":
        registrar_acao(query.from_user, idioma, "Clicou Como Comprar")
        await query.edit_message_text("✅ *Em breve enviaremos as instruções detalhadas de compra.*", parse_mode="Markdown")

# ==================== REGISTRAR VALOR INVESTIDO ===================
async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_valor'):
        valor = update.message.text
        idioma = context.user_data.get("idioma", "en")
        registrar_acao(update.message.from_user, idioma, "Informou Valor", valor)
        await update.message.reply_text(
            f"✅ Investimento *{valor}* registrado com sucesso!",
            parse_mode="Markdown"
        )
        context.user_data['esperando_valor'] = False

# ==================== MAIN APP ====================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_idioma, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT MULTILÍNGUE ONLINE e registrando interações na planilha!")
    app.run_polling()

if __name__ == "__main__":
    main()
