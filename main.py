import datetime
import os
import threading
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ==== CONFIGURAÇÕES ====
BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"  # TOKEN SOBYEN

# URL da planilha SoByen
PLANILHA_NOME = "Investidores_Interessados"  # Deve ser igual ao nome exato da planilha

# Configuração Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open(PLANILHA_NOME).sheet1

# ==== FLASK PARA O RAILWAY ====
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ SoByen Bot está rodando no Railway!"

# ==== MENSAGENS ====
message_pt = """
🚨 *PRÉ-VENDA EXPRESS – SOMENTE 48 HORAS!* 🚨

🔥 *SoByen (SBN)* – Token do agronegócio digital com escassez programada  

✅ Pré-venda: **US$ 0,01**  
✅ Listagem: **US$ 0,02 (lucro imediato 100%)**  
✅ Compra mínima: **US$ 5 | Máxima: US$ 1.000**  
✅ Pagamento: BNB (Rede BSC)

💳 Carteira oficial:
`0x0d5B9634F1C33684C9d2606109B391301b95f002`

⏳ Apenas 48h! Liquidez travada 12 meses
👉 Whitelist (limitada aos 500 primeiros):
https://docs.google.com/forms/d/e/1FAIpQLSfSBNForm/viewform
"""

message_en = """
🔥 *SoByen (SBN)* – Digital agribusiness token with programmed scarcity  

✅ Pre-sale: **US$ 0.01**  
✅ Listing: **US$ 0.02 (instant 100% profit)**  
✅ Min: **US$ 5 | Max: US$ 1,000**  
✅ Payment: BNB (BSC Network)

💳 Official wallet:
`0x0d5B9634F1C33684C9d2606109B391301b95f002`

⏳ Only 48h! Liquidity locked for 12 months
👉 Whitelist (limited to first 500 users):
https://docs.google.com/forms/d/e/1FAIpQLSfSBNForm/viewform
"""

status_msg = """
📊 *Status da Pré-venda SBN*
✅ Preço atual: **US$ 0,01**
✅ Próximo preço: **US$ 0,02**
✅ Duração: Apenas **48h**
✅ Vagas whitelist: **500 primeiras pessoas**
⏳ Restante: **tempo limitado**
"""

outras_ofertas = """
📊 *Outras oportunidades disponíveis:*
✅ Tokens agrícolas em pré-venda
✅ Projetos de energia sustentável
✅ Investimentos tokenizados em commodities

👉 Em breve enviaremos mais detalhes!
"""

# Estado para capturar investimento
user_invest_step = {}

# ==== FUNÇÕES ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Como comprar (PT)", callback_data='pt')],
        [InlineKeyboardButton("🌍 How to buy (EN)", callback_data='en')],
        [InlineKeyboardButton("📈 Status da pré-venda", callback_data='status')],
        [InlineKeyboardButton("📊 Outras oportunidades", callback_data='outras')],
        [InlineKeyboardButton("💰 Informar valor de investimento", callback_data='invest')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✅ *SoByen Bot ativo!* Escolha uma opção abaixo:", reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == 'pt':
        await query.edit_message_text(text=message_pt, parse_mode="Markdown")
        salvar_lead(user, idioma="PT")
    elif query.data == 'en':
        await query.edit_message_text(text=message_en, parse_mode="Markdown")
        salvar_lead(user, idioma="EN")
    elif query.data == 'status':
        await query.edit_message_text(text=status_msg, parse_mode="Markdown")
    elif query.data == 'outras':
        await query.edit_message_text(text=outras_ofertas, parse_mode="Markdown")
    elif query.data == 'invest':
        await query.message.reply_text("💰 *Digite o valor que deseja investir:*", parse_mode="Markdown")
        user_invest_step[user.id] = True

async def registrar_investimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.id in user_invest_step and user_invest_step[user.id]:
        valor = update.message.text
        salvar_investimento(user, valor)
        await update.message.reply_text(f"✅ Registrado! Você informou **{valor}** como valor de investimento.", parse_mode="Markdown")
        del user_invest_step[user.id]

# ==== FUNÇÕES GOOGLE SHEETS ====
def salvar_lead(user, idioma):
    SHEET.append_row([
        user.full_name,
        f"@{user.username}" if user.username else "Sem username",
        idioma,
        "-",
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    ])

def salvar_investimento(user, valor):
    SHEET.append_row([
        user.full_name,
        f"@{user.username}" if user.username else "Sem username",
        "Investimento direto",
        valor,
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    ])

# ==== RODAR TELEGRAM BOT + FLASK PARA RAILWAY ====
def run_telegram():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_investimento))
    print("🤖 BOT SoByen ONLINE e integrado ao Google Sheets!")
    app.run_polling()

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_telegram).start()
    run_flask()
