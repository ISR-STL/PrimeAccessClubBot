import os
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# Token do bot via variável de ambiente (Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# URL da planilha
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1iHuIhFXV4JqZG5XIn_GfbeZJXewR0rWg7SgLD5F_Lfk/edit?usp=sharing"

def conectar_planilha():
    creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = Credentials.from_service_account_info(creds_json, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    return client.open_by_url(PLANILHA_URL).sheet1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem_boas_vindas = (
        "👋 **Bem-vindo(a) ao AgroDigital Club!**\n\n"
        "🌱 Aqui você encontra **oportunidades exclusivas** no agronegócio digital com potencial de crescimento global.\n\n"
        "💡 *Participe da pré-venda do token SoByen (SBN) e garanta posição estratégica no mercado.*\n\n"
        "**Escolha uma opção abaixo para continuar 👇**"
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

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Botões principais
    if query.data == 'pt':
        await query.edit_message_text(
            "🇧🇷 **Pré-venda express do token SoByen (SBN)**\n"
            "📌 Preço pré-venda: **US$ 0,01**\n"
            "📌 Listagem PancakeSwap: **US$ 0,02**\n"
            "📌 Compra mínima: **US$ 5** | Máxima: **US$ 1.000**\n"
            "📌 Pagamento: **BNB (Rede BSC)**\n\n"
            "✅ **Whitelist Oficial:** [Clique aqui para preencher](https://forms.gle/zVJN3BBuZgzCcGB36)",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    elif query.data == 'en':
        await query.edit_message_text(
            "🌍 **SoByen (SBN) Token Flash Pre-Sale**\n"
            "📌 Pre-sale price: **US$ 0.01**\n"
            "📌 PancakeSwap listing: **US$ 0.02**\n"
            "📌 Minimum buy: **US$ 5** | Max: **US$ 1,000**\n"
            "📌 Payment: **BNB (BSC Network)**\n\n"
            "✅ **Whitelist:** [Click here to register](https://forms.gle/zVJN3BBuZgzCcGB36)",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    elif query.data == 'status':
        await query.edit_message_text(
            "📊 **Status da Pré-venda SBN**\n"
            "✅ Preço atual: **US$ 0,01**\n"
            "✅ Próximo preço: **US$ 0,02**\n"
            "✅ Duração: Apenas **48h**\n"
            "✅ Vagas whitelist: **500 primeiras pessoas**"
        )

    elif query.data == 'outros':
        await query.edit_message_text(
            "📌 Temos outras oportunidades de investimento!\n"
            "Em breve enviaremos mais detalhes."
        )

    elif query.data == 'investir':
        # Mostra opções de valores + opção de digitar
        keyboard_valores = [
            [InlineKeyboardButton("$50", callback_data='valor_50')],
            [InlineKeyboardButton("$100", callback_data='valor_100')],
            [InlineKeyboardButton("$500", callback_data='valor_500')],
            [InlineKeyboardButton("$1.000", callback_data='valor_1000')],
            [InlineKeyboardButton("✍️ Outro valor", callback_data='valor_outro')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard_valores)
        await query.edit_message_text(
            "💵 **Escolha um valor para investir ou digite o seu próprio:**",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # Quando ele clicar em valores fixos, registra automaticamente
    elif query.data.startswith("valor_"):
        user = query.from_user
        sheet = conectar_planilha()

        if query.data == "valor_50":
            valor = "50 USD"
        elif query.data == "valor_100":
            valor = "100 USD"
        elif query.data == "valor_500":
            valor = "500 USD"
        elif query.data == "valor_1000":
            valor = "1000 USD"
        elif query.data == "valor_outro":
            await query.edit_message_text(
                "✍️ *Digite o valor que pretende investir (ex.: 750 USD)*",
                parse_mode="Markdown"
            )
            context.user_data['esperando_valor'] = True
            return

        # Registra direto na planilha
        sheet.append_row([
            user.full_name,
            f"@{user.username}" if user.username else "Sem username",
            valor,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ])

        await query.edit_message_text(
            f"✅ Seu investimento de *{valor}* foi registrado com sucesso!",
            parse_mode="Markdown"
        )

async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Quando o usuário escolhe "Outro valor"
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
        await update.message.reply_text(
            f"✅ Investimento *{valor}* registrado com sucesso!",
            parse_mode="Markdown"
        )
        context.user_data['esperando_valor'] = False

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("✅ BOT ONLINE com opções de investimento + integração Google Sheets!")
    app.run_polling()

if __name__ == "__main__":
    main()
