import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from googletrans import Translator  # Tradução automática

# === CONFIGURAÇÕES ===
BOT_TOKEN = "8391268031:AAFbXEi13Zuo6KeExxi21Z2f3fRt9eb5lso"
FORM_BASE = "https://forms.gle/zVJN3BBuZgzCcGB36"

# Logger para debug
logging.basicConfig(level=logging.INFO)
translator = Translator()

# === MENSAGENS BASE ===
mensagens = {
    "pt": {
        "welcome": "🚀 Bem-vindo(a)! Aqui você tem acesso antecipado a *oportunidades exclusivas no mercado digital!* 💎\n\n📈 Escolha abaixo como participar.",
        "how_to_buy": "✅ Como comprar (PT)",
        "status": "📈 Status da pré-venda",
        "offers": "💼 Ver outras ofertas",
        "invest": "💰 Investir agora",
        "status_msg": "📊 *Status da Pré-venda SBN*\n✅ Preço atual: *US$ 0,01*\n✅ Próximo preço: *US$ 0,02*\n✅ Vagas whitelist: *500 primeiras pessoas*\n⏳ Restante: *tempo limitado*",
        "offers_msg": "📌 *Temos novas oportunidades exclusivas chegando!*\n✅ Pré-venda de tokens agrícolas\n✅ Investimentos tokenizados em commodities\n✅ Projetos de impacto sustentável\n\n🚀 *Fique atento, você terá acesso antecipado!*",
        "buy_msg": "🚀 *Pré-venda SoByen (SBN)*\n\n✅ *Preço inicial só para os primeiros 500 investidores*\n✅ *Lucro imediato de +100% ao listar*\n✅ *Pagamento simples via BNB (Rede BSC)*\n\n📌 **Quer prioridade antes que acabe?**\n👉 [Preencha a Whitelist]({form})"
    },
    "en": {
        "welcome": "🚀 Welcome! You now have early access to *exclusive digital market opportunities!* 💎\n\n📈 Choose below to participate.",
        "how_to_buy": "✅ How to buy (EN)",
        "status": "📈 Pre-sale status",
        "offers": "💼 View other offers",
        "invest": "💰 Invest now",
        "status_msg": "📊 *SoByen Pre-sale Status*\n✅ Current price: *US$ 0.01*\n✅ Next price: *US$ 0.02*\n✅ Whitelist spots: *first 500 people*\n⏳ Remaining: *limited time*",
        "offers_msg": "📌 *More exclusive opportunities coming soon!*\n✅ Pre-sale of agricultural tokens\n✅ Tokenized investments in commodities\n✅ Sustainable impact projects\n\n🚀 *Stay tuned for early access!*",
        "buy_msg": "🚀 *SoByen (SBN) Pre-sale*\n\n✅ *Special price for the first 500 investors*\n✅ *Instant +100% profit at listing*\n✅ *Easy payment via BNB (BSC Network)*\n\n📌 **Want priority before it’s gone?**\n👉 [Fill out the Whitelist]({form})"
    },
    "es": {
        "welcome": "🚀 ¡Bienvenido(a)! Ahora tienes acceso anticipado a *oportunidades exclusivas en el mercado digital!* 💎\n\n📈 Elige abajo cómo participar.",
        "how_to_buy": "✅ Cómo comprar (ES)",
        "status": "📈 Estado de la preventa",
        "offers": "💼 Ver otras ofertas",
        "invest": "💰 Invertir ahora",
        "status_msg": "📊 *Estado de la preventa SBN*\n✅ Precio actual: *US$ 0.01*\n✅ Próximo precio: *US$ 0.02*\n✅ Cupos whitelist: *primeras 500 personas*\n⏳ Restante: *tiempo limitado*",
        "offers_msg": "📌 *¡Pronto nuevas oportunidades exclusivas!*\n✅ Preventa de tokens agrícolas\n✅ Inversiones tokenizadas en commodities\n✅ Proyectos de impacto sostenible\n\n🚀 *¡Mantente atento para acceso anticipado!*",
        "buy_msg": "🚀 *Preventas SoByen (SBN)*\n\n✅ *Precio especial para los primeros 500 inversores*\n✅ *Ganancia instantánea del +100% al listar*\n✅ *Pago sencillo vía BNB (Red BSC)*\n\n📌 **¿Quieres prioridad antes que se agote?**\n👉 [Llena la Whitelist]({form})"
    }
}

# === FUNÇÃO PARA DETECTAR IDIOMA ===
def detectar_idioma(user_lang):
    if user_lang.startswith("pt"):
        return "pt"
    elif user_lang.startswith("en"):
        return "en"
    elif user_lang.startswith("es"):
        return "es"
    else:
        return "en"  # fallback inglês

# === /START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = update.message.from_user.language_code or "en"
    idioma = detectar_idioma(lang_code)
    msg = mensagens[idioma]["welcome"]

    keyboard = [
        [InlineKeyboardButton(mensagens[idioma]["how_to_buy"], callback_data=f'buy_{idioma}')],
        [InlineKeyboardButton(mensagens[idioma]["status"], callback_data=f'status_{idioma}')],
        [InlineKeyboardButton(mensagens[idioma]["offers"], callback_data=f'offers_{idioma}')],
        [InlineKeyboardButton(mensagens[idioma]["invest"], url=f"{FORM_BASE}?hl={idioma}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")

# === BOTÕES ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extrai idioma do callback
    data = query.data.split("_")
    action, idioma = data[0], data[1]

    # Ajusta formulário no idioma
    form_link = f"{FORM_BASE}?hl={idioma}"

    if action == "buy":
        await query.edit_message_text(
            mensagens[idioma]["buy_msg"].format(form=form_link),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    elif action == "status":
        await query.edit_message_text(mensagens[idioma]["status_msg"], parse_mode="Markdown")
    elif action == "offers":
        await query.edit_message_text(mensagens[idioma]["offers_msg"], parse_mode="Markdown")

# === MAIN ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ BOT GLOBAL MULTILÍNGUE ONLINE!")
    app.run_polling()

if __name__ == "__main__":
    main()
