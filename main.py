import os
import asyncio
import random
import threading
from flask import Flask
from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler
)

BOT_TOKEN = "8046727069:AAF6wzLZycKZSYOCkx-TJLSkIjRzq7M0a9I"
GROUP_ID = -4823572709
INTERVALO_ENVIO = 3600

MENSAGENS = [
    "🚀 *Atenção!* Uma oportunidade única no mercado digital está aberta apenas para quem está neste grupo. 🔥 Quer entrar antes de todo mundo?",
    "💎 *Lista Premium aberta!* As primeiras vagas garantem benefícios exclusivos. Você vai perder essa chance?",
    "✅ *Investidores inteligentes* já estão garantindo acesso antecipado. Entre agora para não ficar de fora!",
    "📊 O mercado está aquecendo e *quem chegar primeiro leva as maiores vantagens*. Clique no link fixado e participe!",
    "🔥 *Oferta relâmpago!* Somente os membros deste grupo têm prioridade. Garanta seu lugar AGORA!",
    "🌟 Você está a um passo de fazer parte de algo *exclusivo e lucrativo*. Quer saber mais? Fique ligado!",
    "🔒 *Acesso limitado!* Só quem está aqui vai receber os próximos detalhes. Prepare-se para o melhor!",
    "📈 Oportunidades como essa não aparecem duas vezes… *quem decide rápido, colhe primeiro!*",
]

# --- BOT ---
async def gerar_mensagem_en():
    return random.choice(MENSAGENS)

async def envio_automatico(context: ContextTypes.DEFAULT_TYPE):
    msg = await gerar_mensagem_en()
    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=msg,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def start_auto_posting(application):
    job_queue = application.job_queue
    job_queue.run_repeating(envio_automatico, interval=INTERVALO_ENVIO, first=10)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Olá! Eu sou o *PrimeAccessClub Bot*.\n"
        "Estou ativo e pronto para enviar *oportunidades exclusivas* neste grupo! 🚀",
        parse_mode="Markdown"
    )

async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_atual = update.my_chat_member.new_chat_member.status
    if status_atual == "member":
        await update.effective_chat.send_message(
            "👋 Olá! Fui ativado neste grupo para compartilhar *oportunidades premium e exclusivas!* 🔥\n"
            "Fique atento para não perder nada!"
        )

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(ChatMemberHandler(boas_vindas, ChatMemberHandler.MY_CHAT_MEMBER))
    app.post_init(lambda _: asyncio.create_task(start_auto_posting(app)))

    print("✅ BOT ONLINE com mensagens premium automáticas!")
    app.run_polling()

# --- FLASK ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot está rodando no Railway!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

# --- MAIN ---
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
